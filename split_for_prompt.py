import math
#Import file
with open("Input_to_ChatGPT.txt", "r", encoding="utf8") as f:
    contents = f.readlines()

#Analysis of Original dump
print(type(contents)) #List
print(len(contents))

tot_char_length = 0
for x in range(len(contents)):
    elem_length = len(contents[x])
    tot_char_length += elem_length
print("Total length of all elements in full list - ",tot_char_length)
print("")

#############################################################
#Resize the original list and verify if correct
resized_list = []
for x in range(len(contents)):
    chunk= contents[x]
    for letter in chunk:
        resized_list.append(letter)

tot_char_length = 0
for x in range(len(resized_list)):
    elem_length = len(resized_list[x])
    tot_char_length += elem_length
print("Total length of all elements in the resized list - ",tot_char_length)
print("Length of resized_list list -", len(resized_list)) #184262
print("")

#################################################################

final_list = []
char_limit=2000
pre_chunk_tot = math.floor(len(resized_list) / char_limit) + 1 #Round down
print("Total chunks to process (pre-calc) - ", pre_chunk_tot)

begin_text = "The total length of the content that I want to send you is too large to send in only one piece.\
For sending you that content, I will follow this rule: \n \
[START PART 1/{0}]\
 this is the context of the part 1 out of {0} in total \n \
[END PART 1/{0}] \n \
 Then you just answer: \"Received part 1/{0}\" \
 And when I tell you \"ALL PARTS SENT\", then you can continue processing the data and answering my requests. \n  \n ".format(pre_chunk_tot)

for letter in begin_text:
    final_list.append(letter)

chunk_count = 0
char_count=0
temp_chars = []

def split(list_a, chunk_size):
  for i in range(0, len(list_a), chunk_size):
    yield list_a[i:i + chunk_size]

split_resized_list = list(split(resized_list, char_limit))

print("Length of split_resized_list", len(split_resized_list))

sub_list_size = [len(l) for l in split_resized_list if isinstance(l, list) and len(l)> 0]
print("Sublist sizes" , sub_list_size)

for idx, chunk in enumerate(split_resized_list):
    chunk_count += 1
    temp_chars_str= ''.join(map(str, chunk))
    middle_text= " DO not answer yet. This is just another part of the text I want to send you. \
Just receive and acknowledge as \"Part {0}/{1} received\" and wait for the next part \n \
[START PART {0}/{1}] \
 {2} \n\
[END PART {0}/{1}] \n \
Remember not answering yet. Just acknowledge you received this part with the message \"Part {0}/{1} received\" and wait for the next part \n  \n ".format(chunk_count, len(split_resized_list) , temp_chars_str)
    for letter in middle_text:
        final_list.append(letter)

end_text = " ALL PARTS SENT. Now you can continue processing the request. "

for letter in end_text:
    final_list.append(letter)

print("Total number of chunks/parts processed - ", chunk_count)

print("Length of final_list - ", len(final_list))

with open(r"generated_promps.txt", "w") as fp:
    fp.write(''.join(map(str, final_list)))

print("Done")