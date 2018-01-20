import { FooterComponent } from './footer.cmp.js';
import { LoadingComponent } from './loading.cmp.js';
import { NavBarComponent } from './nav-bar.cmp.js';
import { MicronetService } from '../services/micronet.svc.js';
import { UiService } from '../services/ui.svc.js';
import { Message } from '../models/message.js';
import { UtilsService } from '../services/utils.svc.js';
import { Mithril as m } from '../../vendor/js/mithril.js';
import { moment } from '../../vendor/js/moment.js';

export class MessagesComponent {

  constructor() {
    this.api = new MicronetService();
    this.ui = new UiService();
    this.utils = new UtilsService();
    this.p = this.utils.prop;
    this.load();
  }

  onbeforeupdate(){
    if (this.api.messages.length > 0) {
      this.loading = false;
      return true;
    } 
    return false;
  }

  messages() {
    return this.api.messages.map((ms1) => new Message(ms1)).filter((ms2) => ms2.sensor).map((msg3) => this.message(msg3));
  }

  load() {
    this.loading = true;
    this.api.network().then((data) => {
      this.loading = this.api.messages.length <= 0;
      m.redraw();
    });
  }

  message(msg) {
    const t = moment(msg.timestamp).format('dddd, MMMM Do YYYY, h:mm:ss a');
    return m('div.msg', [
      m('div.msg-content', [
        m('span.device', msg.device),
        m('span.sensor-label', msg.sensor.label),
        m('span.sensor-value', msg.sensor.valueLabel)
      ]),
       m('div.msg-timestamp', t)
    ])
  }


  view() {
    let content = m(LoadingComponent);
    if (!this.loading) {
      content = m('main.container', [
        m('h1', 'Messages'),
        this.messages()
      ]);
    }
    return m('article.messages', [
      m(NavBarComponent),
      content,
      m(FooterComponent)
    ]);
  }
}
