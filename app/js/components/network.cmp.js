import { FooterComponent } from './footer.cmp.js';
import { LoadingComponent } from './loading.cmp.js';
import { NavBarComponent } from './nav-bar.cmp.js';
import { MicronetService } from '../services/micronet.svc.js';
import { UiService } from '../services/ui.svc.js';
import { UtilsService } from '../services/utils.svc.js';
import { Device } from '../models/device.js';
import { Mithril as m } from '../../vendor/js/mithril.js';

export class NetworkComponent {

  constructor() {
    this.api = new MicronetService();
    this.ui = new UiService();
    this.utils = new UtilsService();
    this.p = this.utils.prop;
    this.load();
  }

  onbeforeupdate(){
    if (this.p(this.api.data, `devices`)) {
      this.loading = false;
      return true;
    } 
    return false;
  }

  devices() {
    const devices = Object.keys(this.api.data.devices);
    return devices.map((id) => new Device(id, this.api.data.devices[id]));
  }

  load() {
    this.loading = true;
    this.api.network().then((data) => {
      this.loading = !this.p(this.api.data, `devices`);
      m.redraw();
    });
  }

  device(d) {
    const action = this.ui.button({
      icon: 'arrow-right-drop-circle-outline',
      href: `/network/${d.id}`,
      class: 'link'
    });
    return this.ui.tile({
      title: `${d.id} (${d.model})`,
      icon: d.icon,
      subtitle: d.osInfo,
      action: action
    });
  }


  view() {
    let content = m(LoadingComponent);
    if (!this.loading) {
      content = m('main.container', [
        m('h1', 'Devices'),
        m('.columns', this.devices().map((h) => {
          return this.ui.column(this.device(h));
        }))
      ]);
    }
    return m('article.network', [
      m(NavBarComponent),
      content,
      m(FooterComponent)
    ]);
  }
}
