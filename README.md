# NLP-disaster-for-brane

## Extract
extract() loads train.csv, test.csv, and sample_submission.csv into `file:///data/`.

## Visualize
missing_value(source)
Input source as "train" or "test", saves missing value figures as `file:///data/missing_value_[source].png`.

number_of_words(source)
Input source as training set that must containing a "target" column, saves comparison of length of tweets between with disaster or no disaster.

## Preprocessing
cleaning(source)
Input source as "train" or "test", removes link, symbol, emoji, etc. from both training set and testing set, saves output as `file:///data/cleaned_[source].csv`.

precessing(model)
Input model as "train" or "test", tokenizes, and padding the sentences into same length, dump the output as `file:///data/padded_[model].pkl`.

## Model
create()
Creation of the model, save the model as `file:///data/model.h5`.

model_summary(name)
Input name as the output filename, which saves the summary of the keras model, at `file:///data/[name].txt`.

fit(source)
Input source as training dataset, sentences from padded dataset, label from original datasets' column `target`, training 10 epochs, 1/3 of training set are set to validation set. Update model.

predict(source)
Input testing set name as source, reads sentences from padded dataset, uses sample_submission as template to generate the predicted file `file:///data/predicted.csv`, which is ready to be submitted to kaggle.
