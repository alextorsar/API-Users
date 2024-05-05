import pysd
import argparse
from lxml import etree as ET
from xmile_cleaner import clean_xmile
import logging
from pathlib import Path
import os
import glob
from time import perf_counter
import traceback

st = perf_counter()

#Creating argument parser
parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Filename (or pattern) to match XMILE-file(s) to parse",
                    type=str)
parser.add_argument("-si", "--skip-import", dest="skip_import", help="Skip conversion, assume processed file exists",
                    action='store_true', default=False )
parser.add_argument("-sr", "--skip-run", dest="skip_run", help="Skip run after convert",
                    action='store_true', default=False )
parser.add_argument("-v", "--verbose", dest="verbose", help="Output debug information",
                    action='store_true', default=False )
args = parser.parse_args()

impl = logging.getLogger("blib2to3.pgen2.driver")
impl.setLevel(logging.CRITICAL)

# Setup logging
logging.basicConfig(format='%(asctime)s|%(levelname)s\t%(message)s', level=logging.INFO)
if args.verbose:
    logging.getLogger().setLevel(logging.DEBUG)

log = logging.getLogger("polirural-parser")


#Getting file args
files = glob.glob(args.filename)

if not files:
    log.critical("No files matched given filename or pattern")
    exit(-1)
else:
    log.info(files)

for file in files:
    ET.register_namespace(
    'xmile', 'http://docs.oasis-open.org/xmile/ns/XMILE/v1.0')
ET.register_namespace('isee', 'http://iseesystems.com/XMILE')
ns = {
    'xmile': 'http://docs.oasis-open.org/xmile/ns/XMILE/v1.0',
    'isee': 'http://iseesystems.com/XMILE',
}

for xmile_file in files:
    
    file_directory_array = os.path.abspath(xmile_file).replace('\\', '/').split('/')
    file_directory = "/".join(file_directory_array[:-1])
    file_name = file_directory_array[-1].split(".")[0]
    file_extension = file_directory_array[-1].split(".")[1]
    print(os.path.join(file_directory,"clean"))
    os.makedirs(os.path.join(file_directory,"clean"), exist_ok=True)
    os.makedirs(os.path.join(file_directory,"processed"), exist_ok=True)
    cleaned_xmile_filename = os.path.join(file_directory,"clean", "{}_c.{}".format(file_name, file_extension).replace(" ", "_").lower())
    processed_xmile_filename = os.path.join(file_directory,"processed", "{}_p.{}".format(file_name, file_extension).replace(" ", "_").lower())

    if not args.skip_import:
        # Clean input XMILE file
        log.info("Starting cleaning of %s" % xmile_file)
        try:
            clean_xmile(xmile_file, cleaned_xmile_filename)
        except Exception as ex:
            log.error(ex)
            log.error(traceback.format_exc())
            log.error("Failed after %s s, exiting" % (perf_counter() - st))
            exit(-1)

    model_tree = ET.parse(cleaned_xmile_filename)
    model_root = model_tree.getroot()

    for connection in model_root.xpath(".//xmile:model[not(@name)]//xmile:connect", namespaces=ns):
        [target_model_name, target_key_name] = connection.get("to").split(sep=".")
        [source_model_name, source_key_name] = connection.get(
            "from").split(sep=".")

        target_model = model_root.find(
            ".//xmile:model[@name='{}']".format(target_model_name), ns)
        if target_model == None:
            log.error("Could not find target model named '{}'".format(
                target_model_name))
        else:
            variable0 = target_model.find("xmile:variables", ns)
            e0 = variable0.find(
                ".//*[@name='{}']".format(target_key_name.strip('"')), ns)
            if e0 == None:
                log.error(
                    "Could not find target element: {} / {}".format(target_model_name, target_key_name))
            else:
                source_exists = model_root.find(".//xmile:model[@name='{}']/xmile:variables/*[@name='{}']".format(
                    source_model_name, source_key_name.strip('"')), ns)
                if source_exists == None:
                    log.error(
                        "Could not find source element: {} / {}".format(source_model_name, source_key_name))
                else:
                    if target_key_name != source_key_name:
                        log.debug("Updating equation for connection, introducing blind variable: {} - {}".format(
                            target_key_name, source_key_name))
                        eqn0 = e0.find("xmile:eqn", ns)
                        if (eqn0 != None):
                            eqn0.text = "{}".format(source_key_name)
                    else:
                        if not((e0.get("delete_me"))):
                            e0.set("delete_me", "true")
                            log.debug("Flagged {}.{} for deletion".format(
                                target_model_name, target_key_name))
                        else:
                            log.debug("Already flagged for removal")
    elems2del = model_root.findall(".//*[@delete_me='true']", ns)
    if (len(elems2del) > 0):
        log.debug("Found {} elements flagged for deletion".format(len(elems2del)))
        for element in elems2del:
            parent_element = element.find("..", ns)
            if (parent_element == None):
                log.error("Error could not delete {}, could not find parent".format(
                    element.get("name")))
            else:
                log.debug("Removing: {}".format(element.get("name")))
                parent_element.remove(element)
    # Find stocks missing inflows/outflows
    stocks = model_root.xpath(".//xmile:stock", namespaces=ns)
    log.debug("Model contains {} stocks".format(len(stocks)))

    stocks = model_root.xpath(
        ".//xmile:stock[not(.//xmile:inflow) and not(.//xmile:outflow)]", namespaces=ns)
    log.debug("Model contains {} stocks without inflows or outflows".format(len(stocks)))
    for stock in stocks:
        print(stock)
        log.error("The stock '{}' has neiher inflows nor outflows as required by the XMILE standard. Converting to AUX-variables".format(
            stock.get("name")))
        new_aux = ET.Element("aux")
        new_aux.set("name", stock.get("name"))
        for stock_child in stock.findall("./*"):
            new_aux.append(stock_child)
        stock.find("..").append(new_aux)
        try:
            stock.find("..").remove(stock)
            log.debug("Removed stock after introducing aux")
        except e:
            log.error("Failed to remove offending stock")

    # Finding elemnents with duplicate names
    elems_with_name = model_root.xpath(".//*[@name]", namespaces=ns)
    elem_names = []
    for elem in elems_with_name:
        elem_names.append(elem.get("name"))
    seen_elem_names = {}
    duplicate_elem_names = []
    for elem_name in elem_names:
        if elem_name not in seen_elem_names:
            seen_elem_names[elem_name] = 1
        else:
            if seen_elem_names[elem_name] == 1:
                duplicate_elem_names.append(elem_name)
            seen_elem_names[elem_name] += 1

    for duplicate_elem_name in duplicate_elem_names:
        log.error("The name '{}' is used by {} elements in the model".format(
            duplicate_elem_name, seen_elem_names[duplicate_elem_name]))
        first_occurrence = model_root.find(
            ".//*[@name='{}']".format(duplicate_elem_name))
        if (first_occurrence == None):
            log.error("Could not find first occurrence")
        else:
            elem_parent = first_occurrence.find("..", ns)
            if elem_parent != None:
                log.info("Removed element '{}' from model".format(duplicate_elem_name))
                elem_parent.remove(first_occurrence)
            else:
                log.error("Could not remove element {} from model, parent not found".format(duplicate_elem_name))

    model_tree.write(
        processed_xmile_filename,
        xml_declaration=True,
        encoding='utf-8',
        method='xml'
    )
    
    if not args.skip_run:
        try:
            model = pysd.read_xmile(processed_xmile_filename)
        except Exception as e:
            print(repr(e))