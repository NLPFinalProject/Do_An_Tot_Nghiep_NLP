import { Component, OnInit } from '@angular/core';
import { ViewportScroller } from '@angular/common';

import { ThrowStmt } from '@angular/compiler';
import { ScrollToModule } from '@nicky-lenaers/ngx-scroll-to';
import { ScrollToService, ScrollToConfigOptions } from '@nicky-lenaers/ngx-scroll-to';

@Component({
  selector: 'app-test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.scss'],
})
export class TestComponent implements OnInit {
  public data: string;
  public tdata: any;
  private tempdata: any;
  private currentId: string;
  private StoreNumber: number;
  ngOnInit() {
    this.StoreNumber = 0;
    this.tempdata = [
      { id: 10, name: 'Dr Nice' },
      { id: 12, name: 'Narco' },
      { id: 13, name: 'Bombasto' },
      { id: 14, name: 'Celeritas' },
      { id: 15, name: 'Magneta' },
      { id: 16, name: 'RubberMan' },
      { id: 17, name: 'Dynama' },
      { id: 18, name: 'Dr IQ' },
      { id: 19, name: 'Magma' },
      { id: 20, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 11, name: 'Dr Nice' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
      { id: 0, name: 'Tornado' },
    ];
    this.tdata;
    this.tdata = this.tempdata;
    var data3 = "i'm here for yor sake";
    var data2 =
      'Now you diessssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss\nNow you diessssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssNow you diessssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss\nNow you diessssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss';
    console.log('helobo');
    for (var i = 0; i < 5; i++) {
      this.data += data2;
      if (i == 3) i = i;
    }
  }
  HEROES = [
    { id: 11, name: 'Dr Nice' },
    { id: 12, name: 'Narco' },
    { id: 13, name: 'Bombasto' },
    { id: 10, name: 'Celeritas' },
    { id: 15, name: 'Magneta' },
    { id: 16, name: 'RubberMan' },
    { id: 17, name: 'Dynama' },
    { id: 18, name: 'Dr IQ' },
    { id: 19, name: 'Magma' },
    { id: 20, name: 'Tornado' },
    { id: 0, name: 'Tornado' },
    { id: 10, name: 'Tornado' },
    { id: 0, name: 'Tornado' },
    { id: 0, name: 'Tornado' },
    { id: 0, name: 'Tornado' },
    { id: 0, name: 'Tornado' },
    { id: 0, name: 'Tornado' },
    { id: 0, name: 'Tornado' },
  ];

  constructor(private viewportScroller: ViewportScroller) {}
  // get store number - the number of the current same line
  public getCurrentStoreNumber() {
    return this.StoreNumber;
  }
  // get the current line id
  public getCurrentId() {
    return this.currentId;
  }
  public tranformCurrentId(id: string, number: string) {
    if (id == this.currentId) this.tranformCurrentId(id, number);
    else {
      this.currentId = id;
      this.StoreNumber = 0;
    }
  }
  //transform store number to suit the number of the same line
  public TransformMultipleId(str: string, length: number) {
    if (length == 1) return str + '-' + 1;
    else return str + '-' + (this.StoreNumber + 1);
  }
  public onClick(elementId: string): void {
    console.log('here I can');

    //elementId.scrollIntoView();

    this.viewportScroller.scrollToAnchor(elementId);
  }
  public onClick2(elementId: string): void {
    console.log(elementId);
    //this.viewportScroller.scrollToAnchor(elementId);
  }
  /*onClick3($element): void {
    console.log($element);
    $element.scrollIntoView({behavior: "smooth", block: "start", inline: "nearest"});
  }*/
}
