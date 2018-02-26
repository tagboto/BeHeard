# BeHeard
creating a sign language translator using open cv

Over 100 million people, more than 1% of the population have some sort of hearing impairment.
Being deaf from birth, childhood or even later in life many people use sign language as their 
primary form of communication. BeHeard aims to make this communication easier

MY APPROACH
1. Applied a denoising filter to reduce noise in the image 
2. Searched for a specific color in my case a blue glove. And applied a mask to frame
3. Applied another filter to further reduce noise. (dilation filter)
4. Feature Extraction by getting the convex hull value and defects
5. Using Cosine rule to finding the angles and  determine how many fingers were raised thus what sign it is (Marium, Rao, Crasta, Acharya & D'Souza, 2017)

RESULTS.
My program works effectively in the perfect environment however it is still prone to error if the environment is too noisy
It determines the signs used based on the number of fingers held up but can often confuse them
I can so far recognize 5 static signs: B,D,C,5 and I love you


https://drive.google.com/file/d/1kN3XEm8GilWdI_0EFiDbwq9XJmoHtubT/view?usp=sharing
