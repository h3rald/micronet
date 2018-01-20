import { MicronetService } from './services/micronet.svc.js';
import { ConnectComponent } from './components/connect.cmp.js';
import { NetworkComponent } from './components/network.cmp.js';
import { MessagesComponent } from './components/messages.cmp.js';
import { DeviceComponent } from './components/device.cmp.js';
import { Mithril as m } from '../vendor/js/mithril.js';

function init() {
  m.route(document.body, '/network', {
    '/messages': MessagesComponent,
    '/network': NetworkComponent,
    '/network/:id': DeviceComponent,
    '/connect': ConnectComponent
  });
}

init();

