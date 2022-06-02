import preprocessing
import os
import yaml

class Test:
    def __init__(self):
        # Create 2 Files for testing
        train_origin = ["id,keyword,location,text,target\n",
            "1,,,Our Deeds are the Reason of this #earthquake May ALLAH Forgive us all,1\n",
            "4,,,Forest fire near La Ronge Sask. Canada,1\n",
            "5,,,All residents asked to 'shelter in place' are being notified by officers. No other evacuation or shelter in place orders are expected,1\n",
            "143,accident,,only had a car for not even a week and got in a fucking car accident .. Mfs can't fucking drive .,1\n",
            "180,aftershock,304,Sometimes you face difficulties not because you're doing something wrong but because you're doing something right. - Joel Osteen,0\n"]
        with open("./data/train.csv", "w") as f:    
            f.writelines(train_origin)

    def test_cleaning(self):
        os.environ["FILENAME"] = "train"
        os.environ["LOCATION"] = "./data"
        os.environ["COLUMN"] = "text"
        print(preprocessing.cleaning(os.environ["FILENAME"], os.environ["LOCATION"], os.environ["COLUMN"]))
        output = os.system("diff ./data/cleaned_train.csv ./baseline/cleaned_train.csv")
        print(output)
        if output == 0:
            return 0
        else:
            return 1
    def test_processing(self):
        os.environ["FILENAME"] = "train"
        os.environ["LOCATION"] = "./data"
        os.environ["COLUMN"] = "text"
        print(preprocessing.processing(os.environ["FILENAME"], os.environ["LOCATION"], os.environ["COLUMN"]))
        output = os.system("diff ./data/padded_train.pkl ./baseline/padded_train.pkl")
        if output == 0:
            return 0
        else:
            return 1

if __name__ == "__main__":
    a = Test()
    if a.test_cleaning():
        print(yaml.dump({ "contents": "Cleaning [ERROR]"} ))
        exit(1)
    if a.test_processing():
        print(yaml.dump({ "contents": "Processing [ERROR]"} ))
        exit(1)
    else:
        print(yaml.dump({ "contents": "Processing [OK]"} ))
