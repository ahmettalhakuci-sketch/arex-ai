import { registerRootComponent } from 'expo';
import { AppRegistry } from 'react-native';

import App from './App';
import AsistanKoku from './src/Asistan';

// registerRootComponent calls AppRegistry.registerComponent('main', () => App);
// It also ensures that whether you load the app in Expo Go or in a native build,
// the environment is set up appropriately
registerRootComponent(App);
// Yan tuş asistanı: Android'de ayrı şeffaf pencerede (AsistanActivity) açılan Gemini tarzı kart
AppRegistry.registerComponent('asistan', () => AsistanKoku);
