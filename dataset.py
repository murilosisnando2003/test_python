import csv
import argparse
import os

"""
1 - Instructions:
To start the program please run: python dataset2.py --file "data_example.csv"

2 - Project Structure:
    dataset.py - Main file for this project where you find all functions.
    Datasets - Folder that saves all smaller files after split them.
    data_example.csv - file provided as example for this test.

3 - Functions available on this file:
    * split_dataset: Split the main dataset on smaller files
    * read_files: read all smaller files created on save in a dict the result.
    * calculate_result: calculate all posible combinations and shows the result.

"""

## Function that splits the main dataset in smaller files
def split_dataset(csv_file):
    lines_per_file = 30  # Lines on each smaller file
    lines = []  # Stores lines not yet written on a small file
    lines_counter = 0  
    created_files = 0  # Counting how many small files have been created
    with open(csv_file) as big_file:
        for line in big_file:  # Go throught the whole  file
            lines.append(line)
            lines_counter += 1
            if lines_counter == lines_per_file:
                idx = lines_per_file * (created_files + 1)
                with open('Datasets\small_file_%s.csv' % idx, 'w') as small_file:
                    # Write all lines on small file
                    small_file.write('n'.join(lines))
                lines = []  # Reset variables
                lines_counter = 0
                created_files += 1  
        if lines_counter:  # If there are still some lines not written entry here
            idx = lines_per_file * (created_files + 1)
            with open('Datasets\small_file_%s.csv' % idx, 'w') as small_file:
                small_file.write('n'.join(lines))
            created_files += 1
    print ('%s small files (with %s lines each) were created.' % (created_files,lines_per_file)) # print how many samller files was created.
    read_files()

## Function that reads all smaller files and create a unique dict to calculate all posible combinations.
def read_files():
   
    directory = os.path.join(os.getcwd(),"Datasets/")
    # Create a dict to save all baskets.
    baskets = dict()
    # Print columns titles of result
    print('{} | {} | Basket'.format('Product A'.ljust(10), 'Product B'.ljust(10), 'Count'))
    # Walk thru files and save all baskets in splitted datasets.
    for root,dirs,files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                with open(directory + file) as csvfile:
                    # Read csv
                    spamreader = csv.reader(csvfile, delimiter=',')  
                    for row in spamreader:
                        # Variable with basket id and products.
                        basket_id = row[0]
                        product_id =row[1]

                        # Verify if the basket already exists, if not create a new list.
                        if basket_id not in baskets:
                            baskets[basket_id] = list()

                        #Add product in the basket.
                        baskets[basket_id].append(product_id)
    # Call function that calculate the final result.
    calculate_result(baskets)

# Function that calculates all possible combinations based on the dict create before and show the final result.
def calculate_result(baskets):
        
    # Calculate all posible combinations.
    products = dict()
    for basket_id, values in baskets.items():
        for i in range(0, len(values)):
            for j in range(i + 1, len(values)):
                # Create a unique key product x product and start the dictionary on 0 and grows in each interaction.
                key = '{}-{}'.format(values[i], values[j])
                if key not in products:
                    products[key] = 0
                products[key] += 1

    for key, baskets_count in products.items():
        p1, p2 = key.split('-')
        print('{} | {} | {}'.format(p1.ljust(10), p2.ljust(10), baskets_count)) 

## start program the main program    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CSV file.')
    parser.add_argument('--file', type=str, help='CSV file.')
    args = parser.parse_args()
    split_dataset(args.file)

