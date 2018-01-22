import { ConfigService } from "../services/config.svc.js";
import { MicronetService } from "../services/micronet.svc.js";
import { Device } from './device.js';

export class Location {

  constructor(id) {
    this.config = new ConfigService();
    this.api = new MicronetService();
    this.data = this.config.settings.locations[id];
    this.name = this.data.name;
  }

  get devices() {
    return this.data.devices.map((d) => {
      return this.api.data.devices[d] ? new Device(d, this.api.data.devices[d]) : {sensors: {}};
    });
  }

  get sensors() {
    let sensors = [];
    this.devices.forEach((d) => {
      Object.keys(d.sensors).forEach((s1) => {
        d.sensors[s1].forEach((s2) => {
          if (this.config.settings.homeSensors.includes(s2.id)) {
            sensors.push(s2);
          }
        })
      })
    })
    return sensors;
  }
}
