import { Sensor } from './sensor.js';

export class RamSensor extends Sensor {

  constructor(obj, value) {
    super(obj, value);
    this.total = obj.total;
  }

  get rawUsed() {
    const rawTotal = parseInt(this.total.match(/(\d+)/)[1]);
    return this.value*rawTotal/100;
  }

  get used() {
    const rawTotal = parseInt(this.total.match(/(\d+)/)[1]);
    return `${Math.round(this.value*rawTotal)/100}MB`;
  }

  get available() {
    const rawTotal = parseInt(this.total.match(/(\d+)/)[1]);
    return `${Math.round((rawTotal - this.rawUsed)*100)/100}MB`;
  }
}
