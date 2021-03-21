import { ElementRef, Injector } from '@angular/core';
import { MessageService } from '@app/core/services/Utils/message.service';
import { NotificationService } from '@app/core/services/Utils/notification.service';

export abstract class AppComponentBase {
  elementRef: ElementRef;
  messageService: MessageService;
  notificationService: NotificationService;

  constructor(injector: Injector) {
    this.elementRef = injector.get(ElementRef);
    this.messageService = injector.get(MessageService);
    this.notificationService = injector.get(NotificationService);
  }

  l(key: string, ...args: any[]): string {
    // this.localization.localize(key, this.localizationSourceName);
    let localizedText = '';

    if (!localizedText) {
      localizedText = key;
    }

    if (!args || !args.length) {
      return localizedText;
    }

    args.unshift(localizedText);
    // formatString.apply(this, args);
    return '';
  }

  isGranted(permissionName: string): boolean {
    return true;
  }
  //#region Notification
  showSuccessNotification(description: string, title?: string): void {
    this.notificationService.success(description, title);
  }
  showInfoNotification(description: string, title?: string): void {
    this.notificationService.info(description, title);
  }
  showWarningNotification(description: string, title?: string): void {
    this.notificationService.warning(description, title);
  }
  showErrorNotification(description: string, title?: string): void {
    this.notificationService.error(description, title);
  }
  //#endregion

  //#region Message
  showSuccesMessage(message: string): void {
    this.messageService.success(message);
  }

  showWaringMessage(message: string): void {
    this.messageService.warning(message);
  }
  showErrorMessage(message: string): void {
    this.messageService.error(message);
  }
  //#endregion
}
