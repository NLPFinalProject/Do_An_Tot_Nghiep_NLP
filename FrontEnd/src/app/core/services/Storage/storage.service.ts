import { Injectable } from '@angular/core';

@Injectable()
export class StorageService {
  private storage: any;
  constructor() {
    this.storage = localStorage;
  }

  /**
   * Remove and Set value to Local Stograge
   * @param {string} key
   * @param {*} value
   * @memberof StorageService
   */
  removeAndSet(key: string, value: any): void {
    this.remove(key);
    this.set(key, value);
  }

  /**
   * Set value to Local Storage
   * @param {string} key
   * @param {*} value
   * @memberof StorageService
   */
  set(key: string, value: any) {
    this.storage.setItem(key, JSON.stringify(value));
  }

  /**
   * Get value from Local Storage
   * @param {string} key
   * @returns
   * @memberof StorageService
   */
  get(key: string) {
    const item = this.storage.getItem(key);

    if (item && item !== 'undefined') {
      return JSON.parse(this.storage.getItem(key));
    }

    return item;
  }

  /**
   * Remove Value in Local Storage
   * @param {string} key
   * @memberof StorageService
   */
  remove(key: string) {
    this.storage.removeItem(key);
  }
}

export const storageServiceKey = {
  returnUrl: 'returnUrl',
  loggingProfile: 'loggingProfile',
};
