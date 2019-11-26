import pandas as pd 
import numpy as np

#the first thing I did was replicate the datacamp bootstrap replicates functions

#this function is called 1d because it works on one dimension
def bootstrap_replicate_1d(data, func):
    #first points are chosen from the data (with replacement) so that the bootstrap sample
    #has the same number of entries as the original 
    bs_sample = np.random.choice(data, len(data))
    #then a function is applied to that data, e.g. np.mean and that value is returned 
    return func(bs_sample)


def draw_bs_reps(data, func, size=1):
    #here I wanted to use the 1d function to generate many replicates
    #first step is to create an empty array of a specified size
    bs_replicates = np.empty(size)

    # Then I generated replicates using the 1d function and a for loop and store
    #it in the bs_replicates array 
    for i in range(size):
        bs_replicates[i] = bootstrap_replicate_1d(data,func)

    return bs_replicates


#As this is work specific to my project I used a mainguard 
if __name__ == '__main__':
    #here I read in the data but skipped the first 4 rows as they don't hold
    #data 
    df = pd.read_csv('Fish_data.csv', skiprows = 4)
    
   
    #I then got rid of the 'fish' column
    df = df.drop('fish', axis=1)
    

    #the data is now easy to work with and so I started on my analysis
    

    #Referencing the datacamp course, Introduction to Python (NumPy section)
    #I seperated the data into wildtype and mutant
    

    #creating bout_lengths_wt is done by creating a boolean array
    #that tells us whether a Genotype value is wt or not. Then I got all
    #the values in the Bout_Length column that were in the same position
    #as the True values in the Boolean 
    bout_lengths_wt = df['bout_length'][df['genotype'] == 'wt']
    

    #I did the same thing for the mutant types 
    bout_lengths_mut= df['bout_length'][df['genotype'] == 'mut']


    #I then calculated the mean of each of the datasets
    mean_wt = np.mean(bout_lengths_wt)
    mean_mut = np.mean(bout_lengths_mut)

    
    #I then drew bootstrap replicates using the draw_bs_reps function that I had built
    bs_reps_wt = draw_bs_reps(bout_lengths_wt, np.mean, size=10000)
    bs_reps_mut = draw_bs_reps(bout_lengths_mut, np.mean, size=10000)
    

    #I then computed 95% confidence intervals for the bootstrap data.
    #These intervals mean that 95% of the means derived from the bootstrap replicates
    #will lie between these points
    conf_int_wt = np.percentile(bs_reps_wt, [2.5, 97.5])
    conf_int_mut = np.percentile(bs_reps_mut, [2.5, 97.5])
    

    #I changed the wording of the output slightly to make it more reader friendly 
    print("""
    Wildtype: mean = {0:.3f} minutes,  95% confidence interval = [{1:.1f}, {2:.1f}] minutes
    Mutant  : mean = {3:.3f} minutes,  95% confidence interval = [{4:.1f}, {5:.1f}] minutes
    """.format(mean_wt, *conf_int_wt, mean_mut, *conf_int_mut))
