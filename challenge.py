import os
import json
import logging
import argparse

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def read_json_file(file_name):
    """
    Read and parse a JSON files.
    Args:
        file_name (str): Path to the JSON file
    Returns:
        dict: Parsed JSON content
    """
    try:
        # Check if file exists
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"The file {file_name} does not exist.")

        with open(file_name, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON format in {file_name}: {str(e)}")
        
        return data
    
    except FileNotFoundError as e:
        logging.error(f"File Error: {e}")
        raise
    except ValueError as e:
        logging.error(f"Validation Error: {e}")
        raise
    except Exception as e:
        logging.exception(f"Unexpected error reading {file_name}: {e}")
        raise

def generate_output_file(data):

    """
    Reads JSON data, re-format it and saves it as .txt file
    Args:
        data (list): List of dict
    """

    try:
        with open('output.txt', 'w') as file:
            for company in data:
                # Company header
                file.write(f"\nCompany Id: {company['id']}\n")
                file.write(f"Company Name: {company['name']}\n")
                
                # Users Emailed section
                file.write("Users Emailed:\n")
                emailed_users = company.get('users_emailed', [])
                if emailed_users:
                    for user in emailed_users:
                        file.write(f"\t{user['last_name']}, {user['first_name']}, {user['email']}\n")
                        file.write(f"\t\tPrevious Token Balance, {user['tokens']}\n")
                        file.write(f"\t\tNew Token Balance {user['new_token_balance']}\n")
                
                # Users Not Emailed section
                file.write("Users Not Emailed:\n")
                not_emailed_users = company.get('users_not_emailed', [])
                if not_emailed_users:
                    for user in not_emailed_users:
                        file.write(f"\t{user['last_name']}, {user['first_name']}, {user['email']}\n")
                        file.write(f"\t\tPrevious Token Balance, {user['tokens']}\n")
                        file.write(f"\t\tNew Token Balance {user['new_token_balance']}\n")
                
                # Total top-ups (optional)
                if 'total_top_ups' in company:
                    file.write(f"\tTotal amount of top ups for {company['name']}: {company['total_top_ups']}\n")
    
        if os.path.exists('output.txt'):
            logging.info("File 'output.txt' was created successfully!")
        else:
            logging.error("File 'output.txt' was not created.")
    except Exception as e:
            logging.exception(f"An error occurred while writing to 'output.txt': {e}")
            


def main(companies_json_file: str = "companies.json", users_json_file: str = "users.json"):
    """
    Main function responsible for extracting data from JSON files, checking for top up criteria and finally saves the result as output.txt file
    """

    output_data = []
    companies_json_data = read_json_file(companies_json_file)
    users_json_data = read_json_file(users_json_file)
    # Another way but does not handle exceptions
    # users_data = json.load(open(users_json_file))
    for company in companies_json_data:
        try:
            matching_users = [user for user in users_json_data if user['company_id'] == company['id']]
            if matching_users:
                sorted_matching_users = sorted(matching_users, key=lambda x: x['last_name'])
                for user in sorted_matching_users:
                    if user['active_status'] is not False:
                        try:
                            top_up = int(company.get('top_up', 0))
                            tokens = int(user.get('tokens', 0))

                            if tokens < 0:
                                raise ValueError("User tokens cannot be negative.")

                            new_top_up_val = top_up + tokens
                            user['new_token_balance'] = new_top_up_val
                            company.setdefault('total_top_ups', 0)
                            company['total_top_ups'] += top_up

                            if user['email_status'] is not False:
                                company.setdefault('users_emailed', [])
                                company['users_emailed'].append(user) 
                            else:
                                company.setdefault('users_not_emailed', [])
                                company['users_not_emailed'].append(user)
                                
                        except (ValueError, TypeError) as e:
                            logging.error(f"Error adding top-up value: {e}")
                
                output_data.append(company)
            else:
                logging.info(f"The comoany {company['name']} has no users.")
        
        except StopIteration:
            continue
    generate_output_file(output_data)
        


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process companies and users JSON files')
    parser.add_argument('--companies', default='companies.json', 
                        help='Path to companies JSON file')
    parser.add_argument('--users', default='users.json', 
                        help='Path to users JSON file')
    
    args = parser.parse_args()
    main(args.companies, args.users)