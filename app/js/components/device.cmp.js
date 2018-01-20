import { ConfigService } from '../services/config.svc.js';
import { FooterComponent } from './footer.cmp.js';
import { MicronetService } from '../services/micronet.svc.js';
import { LoadingComponent } from './loading.cmp.js';
import { NavBarComponent } from './nav-bar.cmp.js';
import { UiService } from '../services/ui.svc.js';
import { UtilsService } from '../services/utils.svc.js';
import { Device } from '../models/device.js';
import { Mithril as m } from '../../vendor/js/mithril.js';
import { moment } from '../../vendor/js/moment.js';

export class DeviceComponent {

  constructor() {
    this.utils = new UtilsService();
    this.p = this.utils.prop;
    this.id = m.route.param('id');
    this.api = new MicronetService();
    this.config = new ConfigService();
    this.ui = new UiService();
    this.device = {};
    this.dedicatedBlocks = ['cpu', 'ram', 'fs'];
    this.sensors = {};
    this.load();
  }

  onbeforeupdate(){
    if (this.p(this.api.data, `devices.${this.id}`)) {
      this.device = new Device(this.id, this.api.data.devices[this.id]);
      this.loading = false;
      return true;
    } 
    return false;
  }

  load() {
    this.loading = true;
    this.api.device(this.id).then((data) => {
      this.device = data;
      this.loading = !data;
      m.redraw();
    });
  }

  info() {
    return this.ui.panel({
      title: [
        this.ui.icon('information'),
        'Info'
      ],
      body: this.ui.properties({
        Model: this.device.model,
        Kernel: this.device.osInfo
      }),
      footer: ''
    });
  }

  cpu(cpus) {
    const s = cpus[0];
    return this.ui.panel({
      title: [
        this.ui.icon('gauge'),
        'CPU'
      ],
      body: [
        this.ui.properties({
          Frequency: s.frequency,
          Cores: s.cores,
          Usage: s.valueLabel
        })
      ],
      footer: this.ui.meter(s.value)
    });
  }

  ram(mems) {
    const s = mems[0];
    return this.ui.panel({
      title: [
        this.ui.icon('memory'),
        'RAM'
      ],
      body: [
        this.ui.properties({
          Total: s.total,
          Used: s.used,
          Available: s.available
        })
      ],
      footer: this.ui.meter(s.value)
    });
  }

  fs(disks) {
    return this.ui.panel({
      title: [
        this.ui.icon('harddisk'),
        'FileSystem'
      ],
      body: disks.map((disk) => {
        return this.ui.card({
          title: m.trust(disk.diskLabel),
          body: [
            this.ui.properties({
              Total: disk.total,
              Used: disk.used,
              Available: disk.free
            })
          ],
          footer: this.ui.meter(disk.value)
        });
      })
    });
  }
  
  sensorList() {
    return this.ui.panel({
      title: [
        this.ui.icon('access-point'),
        'Sensors'
      ],
      body: [
        this.ui.properties(this.sensors)
      ]
    });
  }


  view() {
    let content = m(LoadingComponent);
    if (!this.loading) {
      const columns = [this.info()];
      this.dedicatedBlocks.forEach((s) => {
        if (this.device.sensors[s]) {
          columns.push(this[s](this.device.sensors[s]));
        }
      })
      Object.keys(this.device.sensors).forEach((s) => {
        console.log(s);
        if (!this.dedicatedBlocks.includes(s)) {
          this.device.sensors[s].forEach((sensor) => {
            this.sensors[sensor.label] = sensor.valueLabel;
          })
        }
      })
      if (Object.keys(this.sensors).length > 0) {
        columns.push(this.sensorList());
      }
      content = m('main.container', [
        m('h1', [
          this.device.icon,
          `${this.device.id} (${this.device.type})`
        ]),
        this.ui.columns(columns)
      ]);
    }
    return m('article.host', [
      m(NavBarComponent),
      content,
      m(FooterComponent)
    ]);
  }
}
