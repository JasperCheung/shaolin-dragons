var key = ""; // Word to achieve; provided by python
var bankSize = 0;
var bankLetters = []; // Letters in the word bank; provided by python
var wordIndex = []; // Indexes of the letter guessed
var category = "";
var isValidating = false;

//---------------------------------------------------------
// INITIALIZATION FUNCTIONS

var setCategory = function(){
  category = location.search.substring(1).split("=")[1]
};

// Fill wordIndex with index values; -1 denotes empty slot
var fillWordIndex = function(){
  for (var i in key){
    wordIndex.push(-1);
  }
};

// Retrieve bank letters and fill bankLetters array
var fillBankLetters = function(){
  for (var i = 0; i < bankSize; i++){
    var id = "bank" + i;
    var letter = document.getElementById(id);
    bankLetters[i] = letter.innerHTML;
  }
};

//---------------------------------------------------------
// ACCESSOR FUNCTIONS

// Check if word guess is full
var isFull = function(){
  for (var i in wordIndex){
    if (wordIndex[i] == -1)
      return false;
  }
  return true;
};

// Check if word guess is empty
var isEmpty = function(){
  for (var i in wordIndex){
    if (wordIndex[i] != -1)
      return false;
  }
  return true;
}

// Return leftmost index of wordIndex whose value is -1
var leftIndex = function(){
  for (var i in wordIndex){
    if (wordIndex[i] == -1)
      return i;
  }
  return -1;
};

// Return rightmost index of wordIndex whose value is not -1
var rightIndex = function(){
  for (var i = wordIndex.length - 1; i > -1; i--){
	  if (wordIndex[i] != -1)
      return i;
  }
  return -1;
};

//---------------------------------------------------------
// WORD VALIDATION FUNCTIONS

// Check for word match when word is complete
var checkWord = function(){
  isValidating = true;
  var guess = "";
  for (var i in wordIndex){
    guess += bankLetters[wordIndex[i]];
  }
  console.log(guess);
  if (key === guess.toLowerCase()){
    changeColor("#26AD2F");
    console.log("isValidating: " + isValidating);
    window.setTimeout(function(){
      changeColor("revert");
      isValidating = false;
      correctWord();
    },700);
  }
  else {
    changeColor("#E84855");
    window.setTimeout(function(){
      changeColor("revert");
      isValidating = false;
      returnLetters();
    },700);
  }
};

// Route to /win which will add 100 points and load new word
var correctWord = function(){
  window.location.href = "/win?category=" + category + "&word=" + key + "&score=100";
};

// Change color of letters to denote correct or incorrect guess
  // Green: #26AD2F
  // Red: #E84855
var changeColor = function(color){
  for (var i in key){
    var id = "word" + i;
    var letter = document.getElementById(id);
    if (color !== "revert")
      letter.setAttribute("style","margin-bottom:10px;background-color:" + color + ";");
    else
      letter.setAttribute("style","margin-bottom:10px;");
  }
};

//---------------------------------------------------------
// LETTER MOVEMENT FUNCTIONS

// Send letter of index i from bank to the the guessed section
var sendLetter = function(i){
  if (isFull())
    return;
  var id = "bank" + i;
  var letter = document.getElementById(id);
  letter.innerHTML = " ";
  letter.setAttribute("class","card-pressed card-letter");
  var j = leftIndex();
  wordIndex[j] = Number(i);
  var wLetter = document.getElementById("word" + j);
  wLetter.innerHTML = bankLetters[i];
  wLetter.setAttribute("class", "card card-letter");
  console.log(wordIndex);
  if (isFull())
    checkWord();
};

// Return a letter of index i from wordIndex to the letter bank
var returnLetter = function(i){
  if (isEmpty() || isValidating){
    return;
  }
  var id = "word" + i;
  var letter = document.getElementById(id);
  letter.innerHTML = " ";
  letter.setAttribute("class","card-pressed card-letter");
  var j = wordIndex[i];
  wordIndex[i] = -1;
  var bLetter = document.getElementById("bank" + j);
  bLetter.innerHTML = bankLetters[j];
  bLetter.setAttribute("class", "card card-letter card-animate");
  console.log(wordIndex);
};

// Return all letters to "bank"
var returnLetters = function(){
  if (isValidating)
    return;
  while (!isEmpty()){
    returnLetter(rightIndex());
  }
};

//---------------------------------------------------------
// EVENT TRIGGER/LISTENER FUNCTIONS

// Run when "bank letters" are clicked to send letter to guessed section
var bankCallback = function(e){
  if (this.getAttribute("class") === "card card-letter card-animate" && !isFull()){
    var i = Number(this.getAttribute("id").substring(4));
    sendLetter(i);
  }
};

// Run when guessed letters are clicked to return letters back to bank
var wordCallback = function(e){
  if (this.getAttribute("class") === "card card-letter"){
    var i = Number(this.getAttribute("id").substring(4));
    returnLetter(i);
  }
};

var flagGIF = function(e) {
    var link = $(this).data("url");
    window.location.href = "/gif_flag?category=" + category + "&word=" + key + "&url=" + link;
}

var flagWord = function(e) {
    window.location.href = "/word_flag?category=" + category + "&word=" + key;
}

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

var addGIFFlagListener = function() {
    $( ".gif-flag" ).click(flagGIF);
}

// Add all event listeners
var addEventListeners = function(){
  addBankListeners();
  addWordListeners();
  addReturnListeners();
  addGIFFlagListener();
};

//---------------------------------------------------------
// KEYBOARD FUNCTIONS

// Check which key is pressed to activate letter movement
$(document).keydown(function(e) {
  var uni = event.which;
  var keyPressed = String.fromCharCode(uni);
  if (uni == 32){
    console.log("Space clicked.");
    returnLetters();
  }
  else if (uni == 8){
    console.log("Backspace clicked.");
    if (rightIndex() != -1)
      returnLetter(rightIndex());
  }
  // else if (uni == 27){
  //   console.log("Escape clicked.");
  //   window.location.href = "/categories";
  // }
  else if (uni >= 49 && uni <= 52){
    console.log(uni);
    $("#modal" + String(uni - 49)).modal("toggle");
  }
  else {
    console.log(keyPressed + " clicked.")
    for (var i in bankLetters){
    	if (keyPressed === bankLetters[i] && document.getElementById("bank" + i).innerHTML !== " "){
        sendLetter(i);
        return;
    	}
    }
  }
});

//---------------------------------------------------------
// SET UP FUNCTIONS

// Gather word information from python and activate setUp()
var retrieveData = function(e){
  $.ajax({
    url: "/play",
    type: "GET",
    data: {},
    success: function(d) {
      console.log(d);
      d = JSON.parse(d);
      key = d["word"];
      bankSize = d["bank_length"];
      setUp();
    }
  })
};

// Word play setup
var setUp = function(){
  setCategory();
  fillWordIndex();
  fillBankLetters();
  addEventListeners();
  console.log("setUp is complete.")
};

retrieveData();
