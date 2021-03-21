export abstract class BaseDto {
  public static fromJSON<T extends BaseDto>(type: { new (): T }, data?: any): T {
    const result = new type();
    result.init(data);
    return result;
  }

  public init(data?: any) {
    if (data) {
      for (const property in data) {
        if (data.hasOwnProperty(property)) {
          (<any>this)[property] = (<any>data)[property];
        }
      }
    }
  }

  public toJSON(data?: any) {
    data = typeof data === 'object' ? data : {};
    for (const property in this) {
      if (this.hasOwnProperty(property)) {
        (<any>data)[property] = (<any>this)[property];
      }
    }
    return data;
  }

  public abstract clone(): any;
}
