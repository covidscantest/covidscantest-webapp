// global options
const VALID_FILE_TYPES = ['image/jpeg', 'image/png'];
const MAX_FILE_SIZE = 2*1024*1024; // 2 MB by default
const UPLOAD_URL = 'https://httpbin.org/post'; // where to send the image


/* global Vue */
// eslint-disable-next-line no-unused-vars
let app = new Vue({

  // the DOM element in which our application exists
  el: '#app',
  delimiters: ['[[',']]'],

  // the "state" of the application
  data: {
    view: 'home', // home | upload | result (what view is visibile)
    image: null, // holds the image when one is dropped or selected
    rawFile: null, // to hold the raw file to upload
    probability: 0, // will be updated with the return value from the data models

    // upload status
    uploading: 0,
    progress: 0,

    // don't change these values,
    // change the ones at the top of the file
    maxSize: MAX_FILE_SIZE,
    validTypes: VALID_FILE_TYPES,
    url: UPLOAD_URL
  },

  // application methods
  methods: {

    // this happens when the form is submitted
    handleFormSubmit: function() {
      if (!this.image) {  
        // no image
        alert('Please select an image to upload.');
      } else {

        // image chosen, do stuff with it
        const file = this.rawFile;
        const xhr = new XMLHttpRequest();

        // final validation before upload
        if (xhr.upload && this.validTypes.includes(file.type) && file.size < this.maxSize) {

          // start the upload
          xhr.open('POST', this.url, true);

          // set listeners to track the progress
          xhr.onprogress = e => {
            if (e.lengthComputable) {
              this.progress = Math.ceil(e.loaded / e.total);
            }
          };

          // upload started, show feedback
          xhr.onloadstart = () => {
            this.uploading = 1;
          };

          // upload done, do the thing
          xhr.onloadend = () => {

            // delay for aesthetics
            setTimeout(() => {
              this.uploading = 2;

              // quick delay for aesthetics
              setTimeout(() => {
                
                // the server's output data will be in res.data;
                // I'm using res.origin.length to generate a random number
                // you would probably want to grab a value out of the data
                const res = JSON.parse(xhr.responseText);
                const probability = Math.ceil(Math.random() * 100);

                this.probability = probability;
                this.view = 'results';
                this.uploading = 0;
                this.progress = 0;

                // this line isn't neccessary
                return res;
              }, 1000);

            }, 2000);
            
          };

          xhr.setRequestHeader('X_FILENAME', file.name);
          xhr.send(file);

        }
      }
    },

    // this handles when a file is chosen
    handleFileInput: function(e) {
      
      const file = e.target.files[0];
      this.rawFile = file;

      // check if the file is an image
      if (this.validTypes.includes(file.type)) {

        // check if the file is less than 2 MB
        if (file.size > this.maxSize) {
          alert('Error: Exceeded max size');
        } else {
          // all good
          const reader = new FileReader();
          reader.onload = f => {
            this.image = f.target.result;
          };

          reader.readAsDataURL(file);  
        }        
      } else {
        alert('Error: Incorrect file type');
      }

    },

    // cancel upload, back to home screen
    cancel: function(view='home') {
      this.view = view;
      this.image = null;
    }
  }

});