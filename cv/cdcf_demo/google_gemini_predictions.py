import os
from google import genai
import time
import pandas as pd
from tqdm import tqdm
import traceback
import argparse
from google.genai.types import Tool, GenerateContentConfig, HttpOptions, UrlContext


#setup argument parser to process command line arguments
parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", type=str, help="Specify an input directory.")
parser.add_argument("-k", "--key", type=str, help="Provide a Google Gemini API Key.")
parser.add_argument("-s", "--start", type=int, help="Specify a starting file number.")
parser.add_argument("-e", "--end", type=int, help="Specify an ending file number.")


args = parser.parse_args()


csv_name = args.file + "_scrape.csv"

df = pd.read_csv(csv_name)



client = genai.Client(api_key=args.key)


image_dir = args.file + "_clean" 

image_list = os.listdir(image_dir)

image_list.sort()

#create a subset of the images in the directory to be processed, each API key can process 200 images per day
image_sub_list = image_list[args.start:args.end]

save_file_name = args.file + "_gemini_predictions_" + str(args.start) + "_" + str(args.end) + ".txt"

save_file = open(save_file_name,"a")



for file in tqdm(image_sub_list):
  if not file == ".DS_Store" and file:

    try:

      #seperate image name to obtain root that was saved in the csv file.
      tag_name = file.rsplit('-', 1)[0]

      #try to locate the row within the csv where that image name is located
      try:
        result_row = df.loc[df['tag'] == tag_name].iloc[0]
      except:
        continue  

      #define the tools used by the model and the prompt
      tools = [{"url_context": {}}]


      prompt = """
          I want you to role play as a Center for Disease Control expert in vaping products. You will be evaluating vape products to determine if they contain a cooling effect, also known as iced. 
          I want you to use the following criteria to evaluate vape products:

          All flavors can be “iced”; that is, the presence of cooling chemical additives that are not the primary flavoring. Many require flavor reviews to confirm, as it is not always evident in the product name. For example, mint ice is most likely a mint flavored product with a cooling sensation, but it may also occasionally be a menthol flavored product.
          If the product flavor name contains cooling suggestion (e.g. Strawberry Ice, Frozen Mint, Cool Watermelon, Chill Mint, etc) = Yes.
          IF NAME DOESN’T INDICATE ICE:   
          If the box and/or advertisement images contain ice imagery (ice cubes, snowflakes, or associated winterized imagery, etc.) = Yes.
          If the box and/or advertisement images contain text that suggest cooling (e.g. Cool Exhale, Iced, Cooling, etc.) = Yes.

          IF IMAGERY DOES NOT INDICATE COOLING PRESENT: 
          Locate flavor review for the searched product. 
          Identify if review mentions any “icy”, “menthol”, “iced”, “cooling sensation”, “chill”, “chilling”, “cool”, etc. 
          If review mentions above terminology = Yes.
          IF NO TERMINOLOGY PRESENT IN REVIEW: 
          If no indication of ice is available after flavor name, imagery, and flavor review search = No 
          NOTE: Flavors like “Strawberry Ice Cream”, “Slushie”, etc. and terms like "Refreshing" don’t always mean that the flavor is iced. For such cases, please look for an indication of coolness in the flavor review, description, or product imagery. Similarly, Mint flavors aren’t always iced unless specified in the name (like “Cool Mint”, “Ice Mint”, etc.) or in the flavor review (“ex: mint with a cooling finish”.

          I have provided you a product image, the webpage for this product is: {} Please use only the image and the webpage to determine if this product produces a cooling effect based on the criteria given, do not use any of the web page search tags as they are not always accurate.

          Do not use any additional websites or sources to make your determination than those given.

          Please provide responses in the following format: yes or no - reason for answer

          """.format(result_row['link'].replace("\n",""))

      #upload the image file to the model to be used as part of answering the question
      my_file = client.files.upload(file=os.path.join(image_dir, file))
      
      #pass the file and prompt to the model and obtain response
      response = client.models.generate_content(
          model="gemini-2.5-flash",
          contents=[my_file, prompt],
          config=GenerateContentConfig(tools=tools, temperature=0.1)
      )


      #seperate the webpage response to determine if it was able to be accessed
      webpage_response = response.candidates[0].url_context_metadata

      #if the response is None that means there was no webpage access, note that and write response to text file
      if webpage_response == None:
        if not response.text == None:
            save_file.write("NO WEBPAGE ACCESS\n")
            save_file.write(file + "\n")
            save_file.write(result_row['link'].replace("\n","") + "\n")
            save_file.write(response.text + "\n")
            save_file.write("-"*60 + "\n")

      else:
          #if the response is not None, then its either success or error, we can now pull the retrieval status
          webpage_access = response.candidates[0].url_context_metadata.url_metadata[0].url_retrieval_status

          #if status was success write the response to the text file
          if "SUCCESS" in str(webpage_access):
            if not response.text == None:
                  save_file.write(file + "\n")
                  save_file.write(result_row['link'].replace("\n","") + "\n")
                  save_file.write(response.text + "\n")
                  save_file.write("-"*60 + "\n")

          #if the status was error, then no webpage was accessed, note that and write response to text file
          elif "ERROR" in str(webpage_access):
            if not response.text == None:
                  save_file.write("NO WEBPAGE ACCESS\n")
                  save_file.write(file + "\n")
                  save_file.write(result_row['link'].replace("\n","") + "\n")
                  save_file.write(response.text + "\n")
                  save_file.write("-"*60 + "\n")

      #pause 15 seconds between queries to ensure we do not exceed the requests per minute
      time.sleep(15)

    #if the model completly fails to run then print out the file name, web link, and the traceback reason for failure.
    #still pause for 15 seconds as we do not want to exceed the requests per minute
    except:
        print("could not run:",file)
        print(result_row['link'].replace("\n",""))
        traceback.print_exc()
        time.sleep(15)




