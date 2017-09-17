import { Sensor } from './sensor.js';

export class FsSensor extends Sensor {

  constructor(obj, value) {
    super(obj, value);
    this.total = obj.total;
    this.device = obj.device;
    this.mount = obj.mount;
  }

  get diskLabel() {
    return `${this.device} &rarr; ${this.mount}`;
  }

  get rawUsed() {
    const rawTotal = parseInt(this.total.match(/(\d+)/)[1]);
    return this.value*rawTotal/100;
  }

  get used() {
    const rawTotal = parseInt(this.total.match(/(\d+)/)[1]);
    return `${Math.round(this.value*rawTotal)/100}GB`;
  }

  get free() {
    const rawTotal = parseInt(this.total.match(/(\d+)/)[1]);
    return `${Math.round((rawTotal - this.rawUsed)*100)/100}GB`;
  }
}
