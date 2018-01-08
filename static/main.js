word = "" // Word to achieve
wordIndex = [] // Refers to the letter inputs for the word to be solved

// Fill wordIndex with index values
var fillWordIndex = function(){
    for (i in word){
	wordIndex.append(-1);
    }    
};

// Check if word is complete 
var checkFull = function(){
    for (i in wordIndex){
	if (wordIndex[i] == -1)
	    return;
    }
    checkWord();
};

// Check for word match
var checkWord = function(){
    guess = ""
    for (i in wordIndex){
	guess += wordIndex[i];
    }
    if (word.equals(guess))
	correctWord();
    else
	returnLetters();
};

// Send all letters to "bank"
var returnLetters = function(){
    return;
};

// Add 100 points to database via python
// Load new word in the same category
var correctWord = function(){
    return;
};

// Run when "bank letters" are clicked
// Send letter to guessed section
var bankClick = function(){
    return;
};

// Run when "guessed letters"  are clicked
// Send letter back to bank
var guessedClick = function(){
    return;
};

// Add listeners to bank letters
var addBankListeners = function(){
    
};

// Add listeners to guessed letters
var addGuessedListeners = function(){

};

// Add listener to return button
var addReturnListeners = function(){

};

// Word play setup
fillWordIndex();
addBankListeners();
addGuessedListeners();
addReturnListeners();
