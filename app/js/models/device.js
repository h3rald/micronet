import { UtilsService } from '../services/utils.svc.js';
import { ConfigService } from '../services/config.svc.js';
import { Sensor } from '../models/sensor.js';
import { RamSensor } from './sensor_ram.js';
import { CpuSensor } from './sensor_cpu.js';
import { FsSensor } from './sensor_fs.js';

export class Device {
  constructor(id, obj) {
    this.rawData = obj;
    this.sensorTypes = {
      'cpu': CpuSensor,
      'ram': RamSensor,
      'fs': FsSensor
    };
    this.utils = new UtilsService();
    this.config = new ConfigService();
    this.p = this.utils.prop;
    this.id = id;
    this.data = obj.data;
    this.info = obj.info;
    this.timestamp = obj.timestamp || 0;
    this.type = this.p(obj, 'info.type');
    this.model = this.p(obj, 'info.model');
    this.os = this.p(obj, 'info.os');
  }

  /*
  {
    fs: [
      {...},
      {...}
    ]
  }
  */
  get sensors() {
    const info = this.p(this.rawData, 'info.sensors');
    if (!info) {
      return {};
    }
    const sensors = Object.keys(info).map((id) => {
      const obj = info[id]
      obj.device = this;
      const constr = this.sensorTypes[obj.type] || Sensor;
      return new constr(obj, this.p(this.rawData, `data.${obj.id}`));
    });
    const sensorGroups = {};
    sensors.forEach((sensor) => {
      if (!sensorGroups[sensor.type]) {
        sensorGroups[sensor.type] = [];
      }
      sensorGroups[sensor.type].push(sensor);
    })
    return sensorGroups;
  }

  get online() {
    return (Date.now() - this.timestamp) < (this.config.settings.onlineTimeout || 20000);
  }

  get icon() {
    let icon = 'desktop-tower';
    if (this.type ===  'microcontroller'){
      icon = 'chip';
    }
    if (this.model.match(/raspberry|C\.?H\.?I\.?P\.?/i)) {
      icon = 'raspberrypi'
    }
    if (this.model.match(/book|laptop/i)) {
      icon = 'laptop';
    }
    if (this.model.match(/vps|server/i)) {
      icon = 'server-network';
    }
    return m(`i.mdi.mdi-${icon}.card-icon.badge.${this.online ? 'online' : 'offline'}`)
  }

  get osInfo() {
    if (this.os) {
      return `${this.os.kernel} ${this.os.version} (${this.os.architecture})`;
    }
    return '';
  }
}
