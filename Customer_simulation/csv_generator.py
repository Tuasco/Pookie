import csv
import random

#TO BE UPDATED WITH NEW ADDITIONAL TRAITS, RERUN TO GET A NEW CSV FILE WITH NEW ADDITIONAL TRAITS

num_rows = 20
base_list = ['rice', 'quinoa', 'bulgur', 'salad']
vft_list = ['avocado' ,'beet' ,'brocoli','carrot','corn','cucumber','dragon fruit','edamame','egg','kiwi','lemon','melon','mint','mushroom','onion','peas','raspberry']
sauce_list = ['sweet soy', 'salty soy', 'yuzu', 'spicy mayo']
protein_list = ['chicken', 'shrimp', 'tofu', 'salmon', 'meat']
trait_list = ['hat', 'glasses'] #ADD new traits


output_file = 'orders_csv.csv'


with open(output_file, mode='w', newline='', encoding='utf-8') as file :
    writer = csv.writer(file)
    
    writer.writerow(['Order_id','Base','VFT', 'Sauce', 'Protein', 'Cooking time', 'Trait'])
    
    
    
    
    for i in range(1, num_rows + 1) :
        
         base = random.choice(base_list)
         sauce = random.choice(sauce_list)
         protein = random.choice(protein_list)
         cooking_time = random.randint(3,10)
         trait = random.choice(trait_list)
         
         vft = random.choices(vft_list, k=random.randint(3,15)) #if we want non-repeating elements, change to random.sample
         vft_all = ';'.join(vft)
         
         writer.writerow([i, base, vft_all, sauce, protein, cooking_time, trait])
         
         
         