import { createApp } from 'vue';
import { createVuetify } from 'vuetify';
import 'vuetify/styles'; // Inclure les styles de Vuetify
import { aliases, mdi } from 'vuetify/iconsets/mdi'; // Charger les icônes mdi
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import App from "@/App.vue";

const vuetify = createVuetify({
    components,
    directives,
    icons: {
        defaultSet: 'mdi',
        aliases,
        sets: {
            mdi,
        },
    },
});

createApp(App).use(vuetify).mount('#app');
