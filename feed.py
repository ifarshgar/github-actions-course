import yaml # Import the PyYAML package
import xml.etree.ElementTree as xml_tree # Import the ElementTree module from the xml.etree package

# Load YAML data from file
with open('feed.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file) # Use the safe_load() function to load the YAML data from the file

# Create RSS element with appropriate attributes and namespaces
rss_element = xml_tree.Element('rss', {'version': '2.0',
                                    'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
                                    'xmlns:content': 'http://purl.org/rss/1.0/modules/content/'})

channel_element = xml_tree.SubElement(rss_element, 'channel') # Create channel element as a child of the RSS element
link_prefix = yaml_data['link'] # Store the link prefix in a variable for convenience

# Add subelements to the channel element using data from the YAML file
xml_tree.SubElement(channel_element, 'title').text = yaml_data['title']
xml_tree.SubElement(channel_element, 'format').text = yaml_data['format']
xml_tree.SubElement(channel_element, 'subtitle').text = yaml_data['subtitle']
xml_tree.SubElement(channel_element, 'itunes:author').text = yaml_data['author']
xml_tree.SubElement(channel_element, 'description').text = yaml_data['description']
xml_tree.SubElement(channel_element, 'itunes:image', {'href': link_prefix + yaml_data['image']})
xml_tree.SubElement(channel_element, 'language').text = yaml_data['language']
xml_tree.SubElement(channel_element, 'link').text = link_prefix

# Create an 'itunes:category' subelement within the 'channel' element, and set its 'text' attribute to the value of the 'category' field from the YAML data
category = xml_tree.SubElement(channel_element, 'itunes:category', {'text': yaml_data['category']})

# Loop through each item in the YAML file's 'item' section, and add an 'item' subelement to the channel element for each one
for item in yaml_data['item']:
    item_element = xml_tree.SubElement(channel_element, 'item')
    xml_tree.SubElement(item_element, 'title').text = item['title']
    xml_tree.SubElement(item_element, 'itunes:author').text = yaml_data['author']
    xml_tree.SubElement(item_element, 'description').text = item['description']
    xml_tree.SubElement(item_element, 'itunes:duration').text = item['duration']
    xml_tree.SubElement(item_element, 'pubDate').text = item['published']
    
    # Add an 'enclosure' subelement to the 'item' element, 
    # which specifies the audio file associated with this item
    enclosure = xml_tree.SubElement(item_element, 'enclosure', {
        'url': link_prefix + item['file'],
        'type': 'audio/mpeg',
        'length': item['length']
    })

# Write the created XML tree to a file
output_tree = xml_tree.ElementTree(rss_element) # Create an ElementTree object from the RSS element
output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True) # Write the XML tree to a file