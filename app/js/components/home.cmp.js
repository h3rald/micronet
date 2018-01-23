import { FooterComponent } from './footer.cmp.js';
import { LoadingComponent } from './loading.cmp.js';
import { NavBarComponent } from './nav-bar.cmp.js';
import { MicronetService } from '../services/micronet.svc.js';
import { UiService } from '../services/ui.svc.js';
import { UtilsService } from '../services/utils.svc.js';
import { Location } from '../models/location.js';
import { Mithril as m } from '../../vendor/js/mithril.js';
import { ConfigService } from '../services/config.svc.js';

export class HomeComponent {

  constructor() {
    this.config = new ConfigService();
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

  locations() {
    return Object.keys(this.config.settings.locations).map((l) => new Location(l));
  }

  location(loc) {
    const sensors = {};
    loc.sensors.forEach((s) => {
      sensors[`<span class="badge ${s.online ? 'online' : 'offline'}">${s.label}</span>`] = s.valueLabel;
    });
    return this.ui.panel({
      title: [
        this.ui.icon('map-marker'),
        loc.name
      ],
      body: [
        this.ui.properties(sensors)
      ]
    });
  }

  view() {
    let content = m(LoadingComponent);
    if (!this.loading) {
      content = m('main.container', [
        m('h1', 'Home'),
        m('.columns', this.locations().map((h) => {
          return this.ui.column(this.location(h));
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
