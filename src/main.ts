import { createApp } from 'vue'

import App from './App.vue'
import router from './router'
import { Amplify } from 'aws-amplify'

Amplify.configure({
  Auth: {
    Cognito: {
      userPoolId: 'us-east-2_LRPKdckjF',
      userPoolClientId: '70mjg0ubnslps0057vp3d74rru',
      loginWith: {
        email: true,
      },
    },
  },
})

createApp(App).use(router).mount('#app')
