import { Injectable } from '@angular/core';
import { NzNotificationService } from 'ng-zorro-antd';

@Injectable()
export class NotificationService {
  constructor(private notification: NzNotificationService) {}

  success(description: string, title?: string): void {
    this.notification.create('success', title != null ? title : 'Thông báo', description);
  }

  info(description: string, title?: string): void {
    this.notification.create('info', title != null ? title : 'Thông báo', description);
  }

  warning(description: string, title?: string): void {
    this.notification.create('warning', title != null ? title : 'Thông báo', description);
  }

  error(description: string, title?: string): void {
    this.notification.create('error', title != null ? title : 'Thông báo', description);
  }
}
