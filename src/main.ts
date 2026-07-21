import { createApp } from 'vue'

import App from './App.vue'
import router from './router'
import { Amplify } from 'aws-amplify'

Amplify.configure({
  Auth: {
    Cognito: {
      userPoolId: 'us-east-2_LRPKdckjF',
      userPoolClientId: '3h67pvo7ah9l4s9c3qqkf6nntj',
      loginWith: {
        email: true,
      },
    },
  },
})

createApp(App).use(router).mount('#app')
