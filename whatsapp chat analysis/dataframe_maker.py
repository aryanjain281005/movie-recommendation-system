import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def parse_whatsapp_chat(data_input):
    # Check if the input is a file path, a file-like object, or a raw string
    if isinstance(data_input, str) and '\n' not in data_input and len(data_input) < 1024:
        with open(data_input, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
    else:
        # If it's a file-like object (like Streamlit UploadedFile)
        if hasattr(data_input, 'read'):
            content = data_input.read()
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            lines = content.splitlines()
        else:
            # It's already the raw text content as a string
            lines = data_input.splitlines()

    # Regex to match the timestamp: e.g., "4/19/26, 10:26 PM - "
    # Uses [\s\u202f] to match both regular spaces and narrow no-break spaces.
    pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4},\s+\d{1,2}:\d{2}[\s\u202f]?[AP]M)\s+-\s+(.*)$'
    
    parsed_data = []
    current_date = None
    current_sender = None
    current_message = []
    
    for line in lines:
        match = re.match(pattern, line)
        
        if match:
            # Append the previous message if exists
            if current_date:
                parsed_data.append({
                    'Date': current_date,
                    'Sender': current_sender,
                    'Message': '\n'.join(current_message)
                })
            
            date_str, rest = match.groups()
            current_date = date_str.replace('\u202f', ' ') # normalize Unicode space
            
            # Check for sender vs system message
            if ': ' in rest:
                current_sender, message = rest.split(': ', 1)
                # Clean up sender name
                current_sender = current_sender.replace('~\u202f', '').replace('~', '').strip()
                current_message = [message]
            else:
                current_sender = 'System'
                current_message = [rest]
        else:
            # Continuation of the previous message
            if current_date:
                current_message.append(line)
                
    # Append final message
    if current_date:
        parsed_data.append({
            'Date': current_date,
            'Sender': current_sender,
            'Message': '\n'.join(current_message)
        })
        
    df = pd.DataFrame(parsed_data)
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y, %I:%M %p')
    return df

