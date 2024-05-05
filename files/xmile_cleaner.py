import re
from lxml import etree as ET
import logging
from lxml import etree

log = logging.getLogger("xmile-cleaner")

def clean_xmile(xmile_file, output_filename):
    print(output_filename)
    """Clean and analyze XMILE file exported from Stella

    Args:
        xmile_file (TextIOWrapper): File handle
        output_xmile_filename_stem (str, optional): Stem of output file

    Returns:
        str: Name of cleaned xmile file
    """
    ET.register_namespace(
        'xmile', 'http://docs.oasis-open.org/xmile/ns/XMILE/v1.0')
    ET.register_namespace('isee', 'http://iseesystems.com/XMILE')

    ns = {
        'xmile': 'http://docs.oasis-open.org/xmile/ns/XMILE/v1.0',
        'isee': 'http://iseesystems.com/XMILE',
    }

    xmile_tree = ET.parse(xmile_file)
    xmile_root = xmile_tree.getroot()


    translated_names = []

    # Regular expressions to detect quoted text
    re_quoted_text2 = r'\"(.+?)\"'

    def clean_string(s):
        return s.replace("\n", "_").replace("\\n", "_").replace(" ", "_") if s != None else s

    def remove_newline(s):
        return s.replace("\n", " ").replace("\r", " ") if s != None else s

    def replace_func(match):
        match = match.group()
        return clean_string(remove_newline(match))

    def append2ntl(from_name, to_name):
        """Append information to name translation list

        Args:
            from_name (str): Name in original file
            to_name (str): Name in output file
        """
        if (from_name != to_name):
            translated_names.append({"from": from_name, "to": to_name})

    def get_elem_info(element):
        """Get information about an LXM element and its parent element

        Args:
            element (lxml.Element): LXML element

        Returns:
            dict: A dictionary with the following keys "parent_element", "parent_localname", "parent_name", "element", "localname", "name"
        """
        parent = element.find("..", ns)
        return {
            "parent_element": parent,
            "parent_localname": ET.QName(parent).localname,
            "parent_name": parent.get("name"),
            "element": element,
            "localname": ET.QName(element).localname,
            "name": element.get("name")
        }
    def remove_isee_elements_from_model(lxml_tree):
        """Remove ISEE specific elements from XMILE

        Args:
            lxml_tree (lxml.etree): [description]
        """
        for isee_elem in lxml_tree.xpath('.//isee:*', namespaces=ns):
            isee_parent = isee_elem.find("..", ns)
            isee_parent.remove(isee_elem)
    
    remove_isee_elements_from_model(xmile_tree)

    # Remove all views from model
    def remove_views_from_model(xml):
        for model in xml.getroot().findall('.//xmile:model', ns):
            for view in model.findall(".//xmile:views", ns):
                model.remove(view)
            if "name" in model.attrib:
                log.debug(model.attrib['name'])
            else:
                log.debug("<Unnamed model>")
    
    remove_views_from_model(xmile_tree)

    # Handle aux
    def clean_named_xmile_elements(xml):
        for aux in xml.getroot().findall('.//xmile:*[@name]', ns):
            aux_name = aux.attrib['name']
            clean_name = clean_string(aux_name)
            aux.attrib['name'] = clean_name
            append2ntl(aux_name, clean_name)

    clean_named_xmile_elements(xmile_tree)

    def clean_inflow_outflow_elements(xml):
        for inoutflow in xmile_root.findall('.//xmile:stock//xmile:inflow|.//xmile:stock//xmile:outflow', ns):
            raw_name = inoutflow.text
            clean_name = clean_string(raw_name)
            inoutflow.text = clean_name
            append2ntl(raw_name, clean_name)
    
    clean_inflow_outflow_elements(xmile_tree)

    # Loop through equations
    def clean_equations(xml):
        for eqn in xml.xpath('.//xmile:model//xmile:eqn', namespaces=ns):
            eqn_text = remove_newline(eqn.text)

            eqn_elem = eqn.find("..", ns)
            elem_info = get_elem_info(eqn_elem)

            if eqn_text == None:
                log.warning("Found element in {}.{} with empty equation '{}'".format(
                    elem_info["parent_name"],
                    eqn_elem.get("name"),
                    eqn_text
                ))
                continue

            if (eqn_text == "{Enter equation for use when not hooked up to other models}"):
                log.warning("Found equation in {}.{} that was not hooked up to model '{}'".format(
                    elem_info["parent_name"],
                    eqn_elem.get("name"),
                    eqn_text
                ))
                eqn_text = eqn_text + "1"
                continue

            # Detect nested statefuls
            if ("DELAY" in eqn_text and "STEP" in eqn_text):
                log.warning("Found nested statefuls in {}.{} in the eqn '{}'".format(
                    elem_info["parent_name"],
                    eqn_elem.get("name"),
                    eqn_text
                ))

            # eqn.text = eqn_text
            if '"' in eqn_text:
                tx2 = re.sub(re_quoted_text2, replace_func, eqn_text)
                if tx2 != eqn_text:
                    log.debug(
                        "Replaced characters inside quoted string in equation: '{}' to '{}'".format(eqn_text, tx2))
                    eqn.text = tx2
    
    clean_equations(xmile_tree)

    to_connections = []
    from_connections = []
    connected_elems = xmile_root.xpath(
        ".//xmile:model//xmile:connect", namespaces=ns)
    for conn_elem in connected_elems:

        from_elem = conn_elem.get("from").split(".")[1]
        from_connections.append(from_elem)

        to_elem = conn_elem.get("to").split(".")[1]
        to_connections.append(to_elem)

        if (from_elem != to_elem):
            log.debug("xmile:connect connects elmeents with different names between models: {} -> {}".format(
                conn_elem.get("from"), conn_elem.get("to")))

    # Find stocks without inflows or outflows
    problem_stocks = xmile_tree.xpath(
        ".//xmile:model/xmile:variables/xmile:stock[not(.//xmile:inflow) and not(.//xmile:outflow)]", namespaces=ns)
    log.error("Found {} stocks without inflows or outflows".format(
        len(problem_stocks)))
    for problem_stock in problem_stocks:
        stock_name = problem_stock.get("name")
        if stock_name in to_connections:
            pass
        else:
            log.error(
                "The stock '{}' has neither inflows nor outflows".format(stock_name))

    # Find element names starting with "not"
    elems_not = xmile_root.xpath(
        ".//xmile:model//*[starts-with(@name,'not')]", namespaces=ns)
    log.error(
        "Found {} elements with names starting with 'not'".format(len(elems_not)))
    for elem_not in elems_not:
        parent_elem = elem_not.find("..", ns)
        elem_info = get_elem_info(elem_not)
        log.error("Element %s.%s starts with 'not' which makes pysd crash",
                  elem_info["parent_name"], elem_info["name"])
        # Find usages of offending term
        usages = xmile_root.xpath(
                ".//*[contains(text(), '{}')]|.//*[contains(@name, '{}')]"
                .format(
                    elem_info["name"],
                    elem_info["name"]
                ), namespaces=ns)
        log.error("--- Found %s usages of: %s" % (len(usages), elem_info["name"]))

        for instance in usages:
            log.error("--- %s.%s@%s", ET.QName(instance).localname,
                      instance.text, instance.get("name"))
            instance.text = instance.text.replace(elem_info["name"], "apfx_%s" % elem_info["name"])
            if (instance.get("name") != None):
                instance.set("name", instance.get("name").replace(elem_info["name"], "apfx_%s" % elem_info["name"]))


    # Finding elemnents with duplicate names
    elems_with_name = xmile_root.xpath(
        ".//xmile:model//*[@name]", namespaces=ns)
    elem_names = []
    for elem in elems_with_name:
        elem_names.append(elem.get("name"))

    # Count duplicates
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
        if (duplicate_elem_name not in to_connections or duplicate_elem_name not in from_connections):
            log.info("The name '{}' is used by {} elements in the model".format(
                duplicate_elem_name, seen_elem_names[duplicate_elem_name]))

    # debug
    # translated_names.sort()
    for name_translation in translated_names:
        log.debug(name_translation)
    try:
        xmile_tree.write(output_filename,
                        xml_declaration=True,
                        encoding='utf-8',
                        method='xml')
    except Exception as e:
        print(e)

    return output_filename
