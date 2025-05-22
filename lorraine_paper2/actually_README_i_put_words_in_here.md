hi this is lorraine here are my notes on the stuff i do in this lorraine_paper2 folder hopefully it helps to make sense of everything. i apologise this is not formal at all, i will clean it up later haha

highlights:
- "*persona*" indicates the model was prompted with the initial lib/conservative alignment and a particular persona as part of the prompt."*base*" refers to prompting the model with only liberal/conservative alignment. "*unaligned*" refers to giving no indication of alignment at all. sometimes *"persona"* may be left out of the filename on accident, but unaligned and base should always be indicated. 
- *raw* data is the data directly spit out by the model/apifunction and can contain between 1-15 trials. *rare* data is the trials in the raw data combined to be all 15 trials in one csv file. *processed* data is the rare data but actually like, formatted and dtyped and with inverses optionally converted and stuff

# model choices
what settings and stuff did you actually use for the models lorraine

## model selection
openai gpt uses gpt4omini set to chat/completions for gpt which is the recommended convo setting as far as i can tell   
- https://platform.openai.com/docs/guides/responses-vs-chat-completions

deepseek uses deepseek-chat   
- https://api-docs.deepseek.com/quick_start/pricing 

anthropic uses claude haiku 3.5 
- https://docs.anthropic.com/en/docs/about-claude/models/overview#model-comparison-table


## temperature
OpenAI GPT model temp range goes from 0.0 - 2.0
- Default is 1.0
- https://community.openai.com/t/does-temperature-go-to-1-or-2/174095/2 

Deepseek model temp range goes from 0.0 - 1.5
- Default is 1.0
- https://api-docs.deepseek.com/quick_start/parameter_settings/ 

Claude model temp range goes from 0.0 - 1.0
- Default is 1.0
- https://docs.anthropic.com/en/api/complete#body-temperature 
- (because claude's default temperature is the max, for the second temp trial i ran it at 0.5)

# naming
what's the originization of your results folder lorraine. great question

## raw vs rare vs processed

***'RAW'*** files are the raw results returned by the ai calling function/batch/etc

***'RARE'*** files are a basic combined version of all 15 trials, processed just enoough to merge 
which basically just means making sure they all have the same columns :P hey do you get it. rare like steak. its 3am and i think im very funny

***'PROCESSED'*** files contain all 15 trials but cleaned up re: dtype, inverse, etc etc

raw/rare/processed are all in their own folders inside results and USUALLY will have RAW/RARE/PROCESSED suffixed to their filename but sometimes i forgot to add it in. man i just realised i should have made processed be like. well done or something. even though well done steak is an insult to steak

## anything important to note about processed files?
yes

high temp models tend to have crazy responses. they will have three response "columns":
- **response** (raw string spit out by the model)
- **response_processed** (first character of the string spit out by the mode, usually a number, sometimes there is no number in which case its a nan value)
- **response_adjusted** (response_processed but with inverse values flipped to correspond to their obverse? value)

the dtypes of the response columns are also a little inconsistent as a result unfortunately:
- a raw response for a high temp question that looks like *"1高手论坛 abertasázurnigstate ru堵注册网址。例如эл解决িশ рассчитedianнатьuyente"* cannot be numerical! 
- in a few cases i couldnt extract a number from a response (you are welcome to look closer at these) and so **response_processed** and **response_adjusted** contain NaN values and the whole column is type float64
- if there were no problems the column usually ended up as int64

### talk more about that response_adjusted thing. what's up with the inverse questions
when working with inverse values you can choose to either work with the raw value or the 'adjusted' output

- for example: the model answers "5" for "it is always wrong to kill another person" and "0" for "it is sometimes okay to kill other people." 
- these questions might both be categorized as "harm" and the second is the inverse of the first. 
- if you were graphing all the "harm" scores for a persona, it would appear to have an average score of ~2.5. 
- the 'adjusted' output converts the answer of "0" to "5," so that when looking at a model's performance across a certain moral foundation and including the inverse the data is more correct.

i'm not explaining this very well but I hope that makes sense. the regular "response" column will have the unadjusted answers to inverse questions; "response_adjusted" will have the flipped/converted answers to inverse questions. the regular questions will be the same in both columns. 

## okay so what do i actually look at to use in the results folder
the initial files in the results folder -- that is, the ones not in *\bin* or *\raw* -- are cleaned up CSV files for each "variation" of model/temperature/alignment. look at those first to use for working with the data

if you find a problem with them then you can go into *\raw* and look at either 
1) a (mostly) raw version of theb data with all 15 trials combined into one file, in the actual subfolders for each model (mostly because i had to add model/temp columns) 

or

2) the actual most raw downloads for each generation-- these had to be split up when generating for sanity and practicality. the amount of trials in each results json/csv will be indicated in the name. these are there if you don't like my processing (which is fine I won't be mad lol) and want to do it yourself


## yeah your processing sucks i'm redoing it. what is going on w this filenaming system though why are there a bunch of letters
lmao real. the files will have the name of the model, the temperature, the question set (graham, which means graham_inverse), the number of trials (x1, 1x, x5, x15), and-- if the trials were split across files-- a string of of equivalent length to the number of trials. 
for example [results_gpt-4o-mini_temp1_graham_x4_FGHI.csv](results/raw/gpt/gpt_temp1.0/results_gpt-4o-mini_temp1_graham_x4_FGHI.csv) has 4 trials and so 4 letters F,G,H,I representing each of those trials

### why are the letters there
 the letters are there for easy distinguishing between which file is which when you are reading and processing and then actually merging them all into one giant file with all 15 trials. i originally used datetime strings but its just slightly rougher on the brain and i found letters easier.

 "O" is the 15th letter of the alphabet btw. 

### i'm looking at your processing code and there are greek letters in here for some reason???? why 
in my earliest processings i was worried i would get confused between files named with an A and variables named with an A. even though yes they correspond. idk it was very late and i wanted to distinguish between the file and the variable holding the processed file. 

i went with the greek alphabet because i'm familar with it but i realised later that well the greek alphabet doesnt match up in order with the english alphabet in a way that is intuitive to most people. for example *gamma Γ* is the third letter of the greek alphabet and so corresponds to *C* but someone else might expect it to correspond to *G* . so i switched back to just using letters for the later processings

we skip lambda bc lambda functions exist, so "pi" is the last greek letter used (even though its 16th in the actual greek alphabet)

### why do some files have results prefixed to them and some don't
files with results prefixed are "raw" files. but i didn't follow this rule religiously so pay more attention to their actual location in the directory