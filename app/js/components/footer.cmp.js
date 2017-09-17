import { ConfigService } from '../services/config.svc.js';
import { MicronetService } from '../services/micronet.svc.js';
import { UtilsService } from '../services/Utils.svc.js';
import { Mithril as m } from '../../vendor/js/mithril.js';

export class FooterComponent {
  
  constructor(){
    this.config = new ConfigService();
    this.api = new MicronetService();
    this.utils = new UtilsService();
  }

  get lastUpdate() {
    const ts = this.utils.prop(this.api, 'data.timestamp');
    if (!ts) {
      return '';
    }
    return m('.last-update', `Last Update: ${new Date(ts).toLocaleString()}`);
  }
  
  view() {
   return m('footer', [
     m('.version', m.trust(`&micro;net v${this.config.version} &mdash; &copy; 2017 Fabio Cevasco`)),
     this.lastUpdate
   ]); 
  }
}
