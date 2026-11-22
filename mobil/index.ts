import { registerRootComponent } from 'expo';
import { AppRegistry, Platform } from 'react-native';

import App from './App';
import AsistanKoku from './src/Asistan';

// registerRootComponent calls AppRegistry.registerComponent('main', () => App);
// It also ensures that whether you load the app in Expo Go or in a native build,
// the environment is set up appropriately
// Web'de ?asistan-onizleme → yan tuş kartını önizle (test için)
const onizleme = Platform.OS === 'web' && typeof location !== 'undefined' && location.search.includes('asistan-onizleme');
registerRootComponent(onizleme ? AsistanKoku : App);
// Yan tuş asistanı: Android'de ayrı şeffaf pencerede (AsistanActivity) açılan Gemini tarzı kart
AppRegistry.registerComponent('asistan', () => AsistanKoku);
