var key = ""; // Word to achieve; provided by python
var bankSize = 16;
var bankLetters = []; // Letters in the word bank; provided by python
var wordIndex = []; // Indexes of the letter guessed
var category = "";

var retrieveKey = function(e){
  $.ajax({
    url: "/play",
    type: "GET",
    data: {},
    success: function(d) {
      console.log(d);
      d = JSON.parse(d);
      key = d["word"];
      setUp();
    }
  })
};

var setCategory = function(){
  category = location.search.substring(1).split("=")[1]
};

// Fill wordIndex with index values
// -1 denotes an empty slot
var fillWordIndex = function(){
  for (var i in key){
    wordIndex.push(-1);
  }
};

// Retrieves bank letters and fills bankLetters array
var fillBankLetters = function(){
  for (var i = 0; i < bankSize; i++){
    var id = "bank" + i;
    var letter = document.getElementById(id);
    bankLetters[i] = letter.innerHTML;
  }
};

// Check if word is complete
var isFull = function(){
  for (var i in wordIndex){
    if (wordIndex[i] == -1)
      return false;
  }
  return true;
};

// Check for word match when word is complete
var checkWord = function(){
  var guess = "";
  for (var i in wordIndex){
    guess += bankLetters[wordIndex[i]];
  }
  console.log(guess);
  if (key === guess.toLowerCase()){
    for (var i in key){
      var id = "word" + i;
      var letter = document.getElementById(id);
      letter.setAttribute("style","margin-bottom:10px;background-color:#26AD2F;")
    }
    window.setTimeout(function(){
      for (var i in key){
        var id = "word" + i;
        var letter = document.getElementById(id);
        letter.setAttribute("style","margin-bottom:10px;")
      }
      correctWord();
    },700);
  }
  else {
    for (var i in key){
      var id = "word" + i;
      var letter = document.getElementById(id);
      letter.setAttribute("style","margin-bottom:10px;background-color:#E84855;")
    }
    window.setTimeout(function(){
      for (var i in key){
        var id = "word" + i;
        var letter = document.getElementById(id);
        letter.setAttribute("style","margin-bottom:10px;")
      }
      returnLetters();
    },700);
  }
};

// Send all letters to "bank"
var returnLetters = function(){
  for (var i in bankLetters){
    var id = "bank" + i;
    var letter = document.getElementById(id);
    letter.innerHTML = bankLetters[i];
    letter.setAttribute("class","card card-letter card-animate");
  }
  for (var i in wordIndex){
    wordIndex[i] = -1;
    var id = "word" + i;
    var letter = document.getElementById(id);
    letter.innerHTML = " ";
    letter.setAttribute("class","card-pressed card-letter");
  }
};

// Add 100 points to database via python
// Load new word in the same category
var correctWord = function(){
  window.location.href = "localhost:5000/game?category=" + category + "&word=" + key + "&score=100";
  // $.ajax({
  //   url: "/win",
  //   type: "GET",
  //   data: {"word" : key, "category" : category}
    // ,
    // success: function(d){
    //   return;
    // }
  // })
};

// Return leftmost index of wordIndex whose value is -1
var leftIndex = function(){
  for (var i in wordIndex){
    if (wordIndex[i] == -1)
      return i;
  }
  return -1;
};

// Run when "bank letters" are clicked
// Send letter to guessed section
var bankCallback = function(e){
  if (this.getAttribute("class") === "card card-letter card-animate" && !isFull()){
    this.innerHTML = " ";
    this.setAttribute("class","card-pressed card-letter");
    // extracting # from id = "bank#" and inserting into wordIndex
    var i = Number(this.getAttribute("id").substring(4));
    var j = leftIndex();
    wordIndex[j] = i;
    letter = document.getElementById("word" + j);
    letter.innerHTML = bankLetters[i];
    letter.setAttribute("class","card card-letter");
    console.log(wordIndex);
    if (isFull())
      checkWord();
  }
};

// Run when "guessed letters" are clicked
// Send letter back to bank
var wordCallback = function(e){
  if (this.getAttribute("class") === "card card-letter"){
    this.innerHTML = " ";
    this.setAttribute("class","card-pressed card-letter");
    var i = this.getAttribute("id").substring(4);
    var j = wordIndex[i]; // j is index of letter in bankLetters
    wordIndex[i] = -1;
    letter = document.getElementById("bank" + j);
    letter.innerHTML = bankLetters[j];
    letter.setAttribute("class","card card-letter card-animate");
  }
};

// Add listeners to bank letters
var addBankListeners = function(){
  for (var i in bankLetters){
    var id = "bank" + i;
    var letter = document.getElementById(id);
    letter.addEventListener("click", bankCallback);
  }
};

// Add listeners to guessed letters
var addWordListeners = function(){
  for (var i in wordIndex){
    var id = "word" + i;
    var letter = document.getElementById(id);
    letter.addEventListener("click", wordCallback);
  }
};

// Add listener to return button
var addReturnListeners = function(){
  var button = document.getElementById("return");
  button.addEventListener("click", returnLetters);
};

// Add all event listeners
var addEventListeners = function(){
  addBankListeners();
  addWordListeners();
  addReturnListeners();
};

// Word play setup
var setUp = function(){
  console.log("setUp has occurred.")
  setCategory();
  fillWordIndex();
  fillBankLetters();
  addEventListeners();
};

retrieveKey();
