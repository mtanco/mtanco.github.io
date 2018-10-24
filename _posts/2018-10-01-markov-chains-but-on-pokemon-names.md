Last week, I had that thing happen where you’re falling asleep, semi-conscious, and then, all of a sudden, you have a GREAT IDEA. I diligently recorded it and then promptly passed out. In the morning, I learned that my SUPER GOOD IDEA was “Markov Chains, but on Pokémon names”.

Which… rhymes so that's cool. I had recently reread the iconic [Tweet Like the President](https://www.kaggle.com/naldershof/tweet-like-the-president-simple-markov) blog post and my subconscious was clearly inspired.

The more I thought about it, the more the idea grew on me. Yes, it’s silly, but the process can be applied to business cases such as segmenting new customers. And thus, the post you’re currently reading. In this post we will use python to:
* Build a Markov Chain of letters for each of the seven Pokémon generations
* For each Pokémon, find the model it fits best in
* Compare our predictions to actual generations
* Invent some new Pokémon
* Determine what generation I would be from if I were a Pokémon

### Import Needed Libraries 

```python
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report,confusion_matrix

%matplotlib inline
```

### Load Pokémon Names Data

In the later generations we get "mega" evolutions, for this reason we want to only keep the default Pokémon


```python
url = 'https://raw.githubusercontent.com/veekun/pokedex/master/pokedex/data/csv/pokemon.csv'
all_pokemon = pd.read_csv(url, index_col = 0)

all_pokemon = all_pokemon[all_pokemon.is_default == 1]

all_pokemon.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>identifier</th>
      <th>species_id</th>
      <th>height</th>
      <th>weight</th>
      <th>base_experience</th>
      <th>order</th>
      <th>is_default</th>
    </tr>
    <tr>
      <th>id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>bulbasaur</td>
      <td>1</td>
      <td>7</td>
      <td>69</td>
      <td>64</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ivysaur</td>
      <td>2</td>
      <td>10</td>
      <td>130</td>
      <td>142</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>venusaur</td>
      <td>3</td>
      <td>20</td>
      <td>1000</td>
      <td>236</td>
      <td>3</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>charmander</td>
      <td>4</td>
      <td>6</td>
      <td>85</td>
      <td>62</td>
      <td>5</td>
      <td>1</td>
    </tr>
    <tr>
      <th>5</th>
      <td>charmeleon</td>
      <td>5</td>
      <td>11</td>
      <td>190</td>
      <td>142</td>
      <td>6</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



### Assign Generations to Each Pokémon


```python
def assign_generation(row):
    if 0 < row['species_id'] <= 151:
        return 'Generation I'
    elif 151 < row['species_id'] <= 251:
        return 'Generation II'
    elif 251 < row['species_id'] <= 386:
        return 'Generation III' 
    elif 386 < row['species_id'] <= 493:
        return 'Generation IV' 
    elif 493 < row['species_id'] <= 649:
        return 'Generation V' 
    elif 649 < row['species_id'] <= 721:
        return 'Generation VI' 
    elif 721 < row['species_id'] <= 807:
        return 'Generation VII' 
    else:
        return 'other'

all_pokemon['generation'] = all_pokemon.apply(assign_generation, axis=1)

all_pokemon.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>identifier</th>
      <th>species_id</th>
      <th>height</th>
      <th>weight</th>
      <th>base_experience</th>
      <th>order</th>
      <th>is_default</th>
      <th>generation</th>
    </tr>
    <tr>
      <th>id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>bulbasaur</td>
      <td>1</td>
      <td>7</td>
      <td>69</td>
      <td>64</td>
      <td>1</td>
      <td>1</td>
      <td>Generation I</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ivysaur</td>
      <td>2</td>
      <td>10</td>
      <td>130</td>
      <td>142</td>
      <td>2</td>
      <td>1</td>
      <td>Generation I</td>
    </tr>
    <tr>
      <th>3</th>
      <td>venusaur</td>
      <td>3</td>
      <td>20</td>
      <td>1000</td>
      <td>236</td>
      <td>3</td>
      <td>1</td>
      <td>Generation I</td>
    </tr>
    <tr>
      <th>4</th>
      <td>charmander</td>
      <td>4</td>
      <td>6</td>
      <td>85</td>
      <td>62</td>
      <td>5</td>
      <td>1</td>
      <td>Generation I</td>
    </tr>
    <tr>
      <th>5</th>
      <td>charmeleon</td>
      <td>5</td>
      <td>11</td>
      <td>190</td>
      <td>142</td>
      <td>6</td>
      <td>1</td>
      <td>Generation I</td>
    </tr>
  </tbody>
</table>
</div>



## Build a Markov Chain

We build a function that takes a series of strings and builds a dictionary of each letter and all letters that follow it - including the end of the word. While looping through the data, we also collect a list of starting letters and get the longest and shortest name.


```python
def build_mc(corpus):
    
    markov_dict = {'<EOT>':[]}
    starting_letters = []
    max_length = 0
    min_length = 1000
    
    for word in corpus:
        tok = list(word) #make character list [l,i,k,e, ,t,h,i,s]
        letter_count = len(tok) #length of word
        
        #storing the max & min values of names
        if(letter_count > max_length):
            max_length = letter_count
        if(letter_count < min_length):
            min_length = letter_count            
        
        for index, letter in enumerate(tok):
            
            #add letter if we haven't yet
            if letter not in markov_dict.keys():
                markov_dict[letter] = []
            
            #add first letters to start list
            if index == 0:
                starting_letters.append(letter)    
            
            #add end of text to last letters of names
            if index == letter_count - 1:
                markov_dict[letter].append("<EOT>")
            #add next letter to non-last letters
            else:
                markov_dict[letter].append(tok[index+1])
                
    return markov_dict, starting_letters, max_length, min_length
```

## Build Markov Chains for each Generation of Pokémon

For each generation we build a seperate model so that we can understand the differences


```python
#hard code for each generation
markov_dict_1, starting_letters_1, max_length_1, min_length_1 = build_mc(all_pokemon[all_pokemon.generation == 'Generation I']['identifier'])
markov_dict_2, starting_letters_2, max_length_2, min_length_2 = build_mc(all_pokemon[all_pokemon.generation == 'Generation II']['identifier'])
markov_dict_3, starting_letters_3, max_length_3, min_length_3 = build_mc(all_pokemon[all_pokemon.generation == 'Generation III']['identifier'])
markov_dict_4, starting_letters_4, max_length_4, min_length_4 = build_mc(all_pokemon[all_pokemon.generation == 'Generation IV']['identifier'])
markov_dict_5, starting_letters_5, max_length_5, min_length_5 = build_mc(all_pokemon[all_pokemon.generation == 'Generation V']['identifier'])
markov_dict_6, starting_letters_6, max_length_6, min_length_6 = build_mc(all_pokemon[all_pokemon.generation == 'Generation VI']['identifier'])
markov_dict_7, starting_letters_7, max_length_7, min_length_7 = build_mc(all_pokemon[all_pokemon.generation == 'Generation VII']['identifier'])

```


```python
# See what follows an x in each generation
print(markov_dict_1['x'])
print(markov_dict_2['x'])
print(markov_dict_3['x'])
print(markov_dict_4['x'])
print(markov_dict_5['x'])
print(markov_dict_6['x'])
print(markov_dict_7['x'])
```

    ['<EOT>', '<EOT>', 'e', 'e', '<EOT>', '<EOT>']
    ['a', '<EOT>']
    ['<EOT>', 'p', 'y']
    ['<EOT>', 'i', 'r', '<EOT>', 'i', 'i']
    ['c', 'e', 'e', 'u', 'o']
    ['e', '<EOT>', '<EOT>', 'e']
    ['<EOT>', 'a', '<EOT>', 'i', 'u']
    

## Generating New Pokémon

We can do random walks on each Markov Chain to invent some new Pokémon - notice the differences in generations, for example we have a lot more dashes in our last generation. 

My personal favorite is telelucry :)


```python
def new_pokemon_name(starting_letter, mc, max_length, min_length):
    
    new_name = starting_letter
    current_letter = starting_letter
    
    while len(new_name) < max_length:        
        next_letter = np.random.choice(mc[current_letter])
        
        #names have to be a least a certain length
        while( (len(new_name) < min_length) & (next_letter == '<EOT>') ):
            next_letter = np.random.choice(mc[current_letter])
        
        if next_letter == '<EOT>':
            return new_name
        
        new_name = new_name + next_letter
        current_letter = next_letter
        
    return new_name
```


```python
print('Generation I')
for x in range(0,5):
    print(new_pokemon_name(np.random.choice(starting_letters_1), markov_dict_1, max_length_1,min_length_1))
print('\nGeneration II')
for x in range(0,5):
    print(new_pokemon_name(np.random.choice(starting_letters_2), markov_dict_2, max_length_2,min_length_2))
print('\nGeneration III')
for x in range(0,5):
    print(new_pokemon_name(np.random.choice(starting_letters_3), markov_dict_3, max_length_3,min_length_3))
print('\nGeneration IV')
for x in range(0,5):
    print(new_pokemon_name(np.random.choice(starting_letters_4), markov_dict_4, max_length_4,min_length_4))
print('\nGeneration V')
for x in range(0,5):
    print(new_pokemon_name(np.random.choice(starting_letters_5), markov_dict_5, max_length_5,min_length_5))
print('\nGeneration VI')
for x in range(0,5):
    print(new_pokemon_name(np.random.choice(starting_letters_6), markov_dict_6, max_length_6,min_length_6))
print('\nGeneration VII')
for x in range(0,5):
    print(new_pokemon_name(np.random.choice(starting_letters_7), markov_dict_7, max_length_7,min_length_7))
```

    Generation I
    buzarolbba
    dable
    sag
    kadugerfau
    chelerage
    
    Generation II
    pipel
    unelu
    traybbawib
    hominury
    hings
    
    Generation III
    sclegoxy
    comush
    bearbecelcoud
    bynamirnhitif
    blothetean
    
    Generation IV
    lirigima-lapak
    powdominoropi
    telelucry
    binoariowdorkr
    chinon
    
    Generation V
    dektya
    serdrm
    vanyetoguandomisshog
    vinsk
    mans
    
    Generation VI
    ddran
    skitzesper
    mpugoo
    annaty
    atedeooninkivabi
    
    Generation VII
    leexuraquzzmuf
    c-olertule
    diangaru
    mileravinitaqu-lu
    pleconnavosorshab
    

## Predict the Generation of Pokémon

Now that we've invented some new Pokés we're going to predict the generation of a Pokémon based just on it's name. Because each model is built on a tiny dataset (80 to 160 names) we are __absolutely going to cheat__ and use models built on the full data set. In the real work we would train test split when checking to see if our models are working or not.

We calculate the probability of one letter following another by going to the key, counting the number of times the next value happens, and dividing this by the total letters. This gives us a precent of the time that one letter follows the next. We then multiply the probabilities together and also multiply this by the probability of the starting letter. 

After getting the likelihood of a word in every model, we choose the most likely as our prediction.

If the word is impossible in every model (for example: 666) it will return "No Prediction".


```python
def generation_probability(word,starting_letters,markov_dict):
    tok_word = list(word)
    letter_count = len(tok_word) #length of word
    probability = 1 

    for index, letter in enumerate(tok_word):
        if(index == 0):
            probability = probability * starting_letters.count('m') / starting_letters.__len__()  
            
        if index == letter_count - 1:
            return probability
        else:
            probability = probability * markov_dict[letter].count(tok_word[index+1]) / markov_dict[letter].__len__()
```


```python
def predicted_generation(row):
    
    probabilities = pd.concat([
        pd.DataFrame([[row['identifier'],'Generation I',generation_probability(row['identifier'],starting_letters_1,markov_dict_1)]]
                    ,columns = ['identifier','generation','probability'])
        ,pd.DataFrame([[row['identifier'],'Generation II',generation_probability(row['identifier'],starting_letters_2,markov_dict_2)]]
                    ,columns = ['identifier','generation','probability'])
        ,pd.DataFrame([[row['identifier'],'Generation III',generation_probability(row['identifier'],starting_letters_3,markov_dict_3)]]
                    ,columns = ['identifier','generation','probability'])
        ,pd.DataFrame([[row['identifier'],'Generation IV',generation_probability(row['identifier'],starting_letters_4,markov_dict_4)]]
                    ,columns = ['identifier','generation','probability'])
        ,pd.DataFrame([[row['identifier'],'Generation V',generation_probability(row['identifier'],starting_letters_5,markov_dict_5)]]
                    ,columns = ['identifier','generation','probability'])
        ,pd.DataFrame([[row['identifier'],'Generation VI',generation_probability(row['identifier'],starting_letters_6,markov_dict_6)]]
                    ,columns = ['identifier','generation','probability'])
        ,pd.DataFrame([[row['identifier'],'Generation VII',generation_probability(row['identifier'],starting_letters_7,markov_dict_7)]]
                    ,columns = ['identifier','generation','probability'])
    ])
    
    highest_prob = probabilities['probability'].max()
    
    if(highest_prob == 0):
        return 'No Prediction'
#         return np.random.choice(['Generation I','Generation II','Generation III'
#                  ,'Generation IV', 'Generation V', 'Generation VI','Generation VII'])
    
    return probabilities[probabilities.probability == highest_prob]['generation']
    
```


```python
all_pokemon['prediction'] = all_pokemon.apply(predicted_generation, axis=1)
```

#### We've Got Impressive Results!

If we were to just guess the generation randomly, we would expect accuracies of ~1/7 or 14%. We know that we are giving the models a big advantage by training and testing on the same data. Even so, our prediction results are much much better than 14%. It's tempting to then claim that the names of Pokémon really did change from season to season, we proved it! And yes, there were some changes like longer names and more dashes. However, our training data sets are so tiny that we definitely just have over fitted models :) 


```python
print(classification_report(all_pokemon.generation,all_pokemon.prediction))
```

                    precision    recall  f1-score   support
    
      Generation I       0.69      0.72      0.70       151
     Generation II       0.67      0.64      0.65       100
    Generation III       0.77      0.70      0.73       135
     Generation IV       0.59      0.80      0.68       107
      Generation V       0.88      0.59      0.71       156
     Generation VI       0.80      0.74      0.77        72
    Generation VII       0.59      0.79      0.67        86
    
       avg / total       0.72      0.70      0.70       807
    
    


```python
print(confusion_matrix(all_pokemon.generation,all_pokemon.prediction))
```

    [[108   9   6  14   2   2  10]
     [  8  64   4  13   2   2   7]
     [  8   7  94  14   3   3   6]
     [  5   5   2  86   0   1   8]
     [ 18   4  11  10  92   4  17]
     [  5   4   4   4   2  53   0]
     [  5   3   1   5   3   1  68]]
    

## What Generation of Pokémon Am I ???

Finally, let's take some non-pokemon words and see what generation they are most likely to be from


```python
mt = pd.DataFrame(['michelle','tanco','hunter','teradata','xx'], columns =['identifier'])
```


```python
mt['generation'] = mt.apply(predicted_generation, axis=1)
```


```python
mt
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>identifier</th>
      <th>generation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>michelle</td>
      <td>Generation IV</td>
    </tr>
    <tr>
      <th>1</th>
      <td>tanco</td>
      <td>Generation VII</td>
    </tr>
    <tr>
      <th>2</th>
      <td>hunter</td>
      <td>Generation II</td>
    </tr>
    <tr>
      <th>3</th>
      <td>teradata</td>
      <td>Generation I</td>
    </tr>
    <tr>
      <th>4</th>
      <td>xx</td>
      <td>No Prediction</td>
    </tr>
  </tbody>
</table>
</div>


