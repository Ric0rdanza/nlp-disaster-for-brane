# NLP-disaster-for-brane

## Extract
extract(location: str) loads train.csv, test.csv, and sample_submission.csv into given location under `file://`.
E.g. `extract("/data")` => `file:///data/`

## Visualize
missing_value(filename, location, column_1, column_2, column_3, column_4, column_5)
Input location and name of a file, as well as column name to be illustrated, saves missing value figures as `file://{location}/missing_value_{filename}.png`.
column_n means column name to be inspected, up to 5 columns available. Use "-" if less than 5 columns to inspect.
E.g. `missing_value("train", "/data", "location", "keyword", "-", "-", "-")` => `file:///data/missing_value_train.png`

number_of_words(filename, location, column, column_target)
Input location, name of a file and the column name of text to count word, and target column name (0 and 1 only) as the training set, save comparison of length of tweets between target 0 and 1.
E.g. `number_of_words("train", "/data", "text", "target")` => `file:///data/number_of_words_train.png`


## Preprocessing
correlation(filename, location, column_1, column_2, method)
Input a filename and its location, and calculate the correlation of column_1 and column_2 with a different method, which currently supports Spearman correlation and Pearson correlation.
E.g. `correlation("file", "/data", "location", "target", "spearman")` => `0.05`(a double precision floating number as string)

cleaning(filename, location, column)
Input file, removes link, symbol, emoji, etc. from column, saves output as `file://{location}/cleaned_{filename}.csv`.

precessing(filename, location, column)
Input a file tokenizes, and padding the sentences into same length, dump the output as `file://{location}/padded_{filename}.pkl`.

## Model
create(location)
Creation of the model, save the model as `file://{location}/model.h5`.

model_summary(filename, location)
Input a filename, which saves the summary of the keras model, at `file://{location}/{filename}.txt`.

fit(filename, location)
Input a training dataset's filename and location, which contains column `target`, training 10 epochs, 20% of the training set are used for the validation.

predict(filename, location)
Input testing set's filename and location use sample_submission as a template to generate the predicted file `file://{location}/predicted.csv`, which is ready to be submitted to Kaggle.
