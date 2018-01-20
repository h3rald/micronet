import { ConfigService } from '../services/config.svc.js';
import { Mithril as m } from '../../vendor/js/mithril.js';
import { moment } from '../../vendor/js/moment.js'; 
import {TabBarComponent as TabBar} from './tabbar.cmp.js';

export class FooterComponent {
  
  constructor(){
    this.config = new ConfigService();
    this.tabs = [];
    this.tabs.push({
      title: 'Devices',
      selected: m.route.get().match(/^\/network/),
      icon: 'server',
      callback: () => {
        m.route.set(`/network`);
      }
    });
    this.tabs.push({
      title: 'Messages',
      selected: m.route.get().match(/^\/messages/),
      icon: 'message-text-outline',
      callback: () => {
        m.route.set(`/messages`);
      }
    });
  }

  view() {
   return m('footer', [
     m(TabBar, {tabs: this.tabs}),
     m('.version', m.trust(`&micro;net v${this.config.version} &mdash; &copy; ${new Date().getFullYear()} Fabio Cevasco`))
   ]); 
  }
}
