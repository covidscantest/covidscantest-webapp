/* global Vue */

const app = new Vue({

  // element where the app lives
  el: '#app',
  delimiters: ['[[',']]'],

  // app state
  data: {
    isActive: true,
    image: null,
    file: null,

    // image specs
    validTypes: ['image/jpeg', 'image/png'],
    maxSize: 2 * 1024 * 1024, // 2 MB
    url: 'result/',

    // user acknowledgements
    notForMedicalUse: false,
    privacyPolicy: false,

    // upload status
    uploading: false,
    results: null
  },

  // computed values
  computed: {
    output() {
      const LOOKUP = {
        'healthy_prob': 'Healthy lungs',
        'pneumonia_prob': 'Pneumonia',
        'covid_prob': 'COVID-19',
        'rest_prob': 'Other'
      };

      return Object.entries(this.results || {})
        .filter(([check]) => check !== 'xray_prob')
        .map(([check, value]) => {
          return [
            LOOKUP[check],
            `${(value * 100).toFixed(2)}%`,
            value < 0.3
              ? 'low'
              : value < 0.6
                ? 'med'
                : 'high'
          ];
        });
    }
  },

  // app methods and lifecycle stuff
  methods: {
    clearImage() {
      document.querySelector('input[type=file').value = '';
      this.file = null;
      this.image = null;
      this.results = null;
      this.isActive = false;
    },

    handleImage(e) {
      e.preventDefault();
      const file = e.target.files[0];

      // check if the file is an image
      if (this.validTypes.includes(file.type)) {

        // check if the file is less than 2 MB
        if (file.size > this.maxSize) {
          alert('Error: Exceeded max size');
          return false;
        } else {
          // all good
          const reader = new FileReader();
          reader.onload = f => {
            this.image = f.target.result;
            this.file = file;
          };

          reader.readAsDataURL(file);  
        }        
      } else {
        alert('Error: Incorrect file type');
        return false;
      }
    },

    // upload it
    handleSubmit() {

      const formData = new FormData();
      formData.append('image', this.file);
      
      this.uploading = true;
      fetch(this.url, {
        method: 'POST',
        body: formData
      })
        .then(res => res.json())
        .then(data => {
          this.results = data;
          this.uploading = false;
        });

    }


  }

});