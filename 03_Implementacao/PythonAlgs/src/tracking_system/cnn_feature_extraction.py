import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from torch.autograd import Variable
from PIL import Image
import time

# Load the pretrained model
model = models.resnet18(pretrained=True)
# Use the model object to select the desired layer
layer = model._modules.get('avgpool')

# Set model to evaluation mode
model.eval()

scaler = transforms.Resize((224, 224))
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
to_tensor = transforms.ToTensor()

def get_vector(frame):
    # 1. Load the image with Pillow library
    img = Image.fromarray(frame)
    # 2. Create a PyTorch Variable with the transformed image
    t_img = Variable(normalize(to_tensor(scaler(img))).unsqueeze(0))
    # 3. Create a vector of zeros that will hold our feature vector
    #    The 'avgpool' layer has an output size of 512
    my_embedding = torch.zeros(512)
    # 4. Define a function that will copy the output of a layer
    def copy_data(m, i, o):
        my_embedding.copy_(o.data.squeeze())
    # 5. Attach that function to our selected layer
    h = layer.register_forward_hook(copy_data)
    # 6. Run the model on our transformed image
    model(t_img)
    # 7. Detach our copy function from the layer
    h.remove()
    # 8. Return the feature vector
    return my_embedding


def calc_distance(lista, listb):
    return sum( (b - a) ** 2 for a,b in zip(lista, listb) ) ** .5

##v1 = get_vector("70.jpg")
##print(v1)

def get_distance(img2):
    
    v2 = get_vector(img2)
    return calc_distance(v1, v2)

##loc = "person_frames/"
##distance = 10000
##
##
##import os
##
##for filename in os.listdir("person_frames"):
##    if filename.endswith(".jpg"): 
##        d = get_distance("person_frames/"+filename)
##        if d<distance:
##            distance=d
##            print(filename)
   

    
    




