export class Sensor {

  constructor(obj, value) {
    this.freq = obj.freq;
    this.id = obj.id;
    this.label = obj.label;
    this.type = obj.type;
    this.device = obj.device;
    this.value = value;
    this.uom = obj.uom;
  }

  get online() {
    return this.device.online;
  }

  get valueLabel() {
    return `${this.value}${this.uom}`;
  }
}
