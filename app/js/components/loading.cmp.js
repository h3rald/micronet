import { Mithril as m } from '../../vendor/js/mithril.js';

export class LoadingComponent {

  view() {
   return m('main.loading-data', [
      m('.loading'),
      m('.centered.centered-text', 'Loading...')
    ]); 
  }
}
