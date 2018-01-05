import { ConfigService } from '../services/config.svc.js';
import { FooterComponent } from './footer.cmp.js';
import { MicronetService } from '../services/micronet.svc.js';
import { LoadingComponent } from './loading.cmp.js';
import { NavBarComponent } from './nav-bar.cmp.js';
import { UiService } from '../services/ui.svc.js';
import { UtilsService } from '../services/utils.svc.js';
import { Device } from '../models/device.js';
import { Mithril as m } from '../../vendor/js/mithril.js';

export class DeviceComponent {

  constructor() {
    this.utils = new UtilsService();
    this.p = this.utils.prop;
    this.id = m.route.param('id');
    this.api = new MicronetService();
    this.config = new ConfigService();
    this.ui = new UiService();
    this.device = {};
    this.knownSensors = ['cpu', 'ram', 'fs', 'bme280', 'dht11'];
    this.additionalSensors = {};
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

  dht11(dht) {
    return this.ui.panel({
      title: [
        this.ui.icon('weather-partlycloudy'),
        'DHT11'
      ],
      body: [
        this.ui.properties({
          Temperature: dht.find((v) => v.id === 'temperature').valueLabel,
          Humidity: dht.find((v) => v.id === 'humidity').valueLabel
        })
      ]
    });
  }

  bme280(bme) {
    return this.ui.panel({
      title: [
        this.ui.icon('weather-partlycloudy'),
        'BME280'
      ],
      body: [
        this.ui.properties({
          Temperature: bme.find((v) => v.id === 'temperature').valueLabel,
          Pressure: bme.find((v) => v.id === 'pressure').valueLabel,
          Humidity: bme.find((v) => v.id === 'humidity').valueLabel
        })
      ]
    });
  }

  additional() {
    return this.ui.panel({
      title: [
        this.ui.icon('access-point'),
        'Other Sensors'
      ],
      body: [
        this.ui.properties(this.additionalSensors)
      ]
    });
  }


  view() {
    let content = m(LoadingComponent);
    if (!this.loading) {
      const columns = [this.info()];
      this.knownSensors.forEach((s) => {
        if (this.device.sensors[s]) {
          columns.push(this[s](this.device.sensors[s]));
        }
      })
      Object.keys(this.device.sensors).forEach((s) => {
        console.log(s);
        if (!this.knownSensors.includes(s)) {
          this.device.sensors[s].forEach((sensor) => {
            this.additionalSensors[sensor.label] = sensor.valueLabel;
          })
        }
      })
      if (Object.keys(this.additionalSensors).length > 0) {
        console.log(Object.keys(this.additionalSensors))
        columns.push(this.additional());
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
