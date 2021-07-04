import { Component, OnInit, Input } from '@angular/core';
import { MessageService } from '@app/core/services/Utils/message.service';
import { ScrollToService, ScrollToConfigOptions } from '@nicky-lenaers/ngx-scroll-to';
import { ViewportScroller } from '@angular/common';
import { DaovanServiceService } from '../../daovan-service.service';
@Component({
  selector: 'app-diff-content',
  templateUrl: './diff-content.component.html',
  styleUrls: ['./diff-content.component.scss'],
})
export class DiffContentComponent implements OnInit {
  @Input() SessionData: any;
  sortValue: any = null;
  public currentId: number;
  public storeNumber: number = 0;
  public storeCurrentLength: number = 0;
  sortName: any = null;
  private sameline: any[];
  public answer: any;
  public ratio: any;
  listOfSearchName: any = [];
  searchAddress: string;
  displayData1: Array<any> = [];
  displayData2: Array<object> = [];
  loading = true;
  isChangeFlag: boolean = false;
  //
  fileList: Array<object> = [];
  constructor(
    private messageService: MessageService,
    private viewportScroller: ViewportScroller,
    private scrollToService: ScrollToService,
    private DaoVanService: DaovanServiceService
  ) {}
  ngOnInit(): void {
    this.answer = {
      ls1: [],
      ls2: [],
      ls3: [],
    };

    this.DaoVanService.sendMessage.subscribe((data: any) => {
      console.log(data);
    });

    this.doStep();
    this.DaoVanService.sendMessageNumber.subscribe((data: number) => {
      this.ratio = 0;
      this.isChangeFlag = false;

      this.ShowResult(data);
    });
  }
  doStep() {
    this.getFirstSentences();
    this.ShowResult(0);
    this.getData();
  }
  getFirstSentences() {
    if (this.SessionData != null) {
      // this.file1Name = this.data.File1Name;
      let tempdata = [];
      let temp: {
        id: number;
        data: string;
      };

      for (var i = 0; i < this.SessionData.file1.length; i++) {
        temp = {
          id: i + 1,
          data: this.SessionData.file1[i],
        };
        tempdata.push(temp);
      }
      this.answer.ls1 = tempdata;
    } else {
    }
  }
  ngOnChanges() {
    //this.childFunction()
    this.storeCurrentLength = 0;
    this.doStep();
  }
  ShowResult(num: number) {
    this.sameline = [];

    let data = this.SessionData;
    //console.log(this.data);

    if (this.SessionData != null) {
      let temp: {
        id: number;
        data: string;
      };
      let index = 0;
      for (var i = 0; i < this.SessionData.file1.length; i++) {
        if (this.SessionData.ListFile[num].stt[i] != undefined) {
          for (var j = 0; j < this.SessionData.ListFile[num].stt[i][1]; j++) {
            console.log(this.SessionData.ListFile[num].stt[i][2][j]);
            if (this.sameline.indexOf(this.SessionData.ListFile[num].stt[i][2][j]) === -1) {
              this.sameline.push(this.SessionData.ListFile[num].stt[i][2][j]);
            }
          }
        }
      }

      let tempdata2 = [];
      for (var i = 0; i < this.SessionData.ListFile[num].data.length; i++) {
        temp = {
          id: index + 1,
          data: this.SessionData.ListFile[num].data[i],
        };
        tempdata2.push(temp);
        index = index + 1;
      }
      this.answer.ls2 = tempdata2;
      this.answer.ls3 = data.ListFile[num].stt;

      this.displayData2 = this.answer.ls2;
    } else {
    }
  }

  getData(): void {
    const number = Math.floor(Math.random() * 100);
    setTimeout(() => {
      this.displayData1 = [...this.answer.ls1];
      console.log(this.answer);
      console.log(this.answer.ls2);
      this.displayData2 = [...this.answer.ls2];
      this.loading = false;
    }, number);
  }
  triggerScrollTo(id: number) {
    this.isChangeFlag = true;
    if (this.currentId != id) {
      this.currentId = id;
      this.storeCurrentLength = 0;
      this.storeNumber = 0;
    }
    this.storeCurrentLength = 0;
    id = id - 1;
    console.log(id);
    let element = this.answer.ls3[id];
    if (element[1] != null) {
      this.storeCurrentLength = element[1];
      console.log('number of same line is');
      console.log(this.storeCurrentLength);
    }

    this.ratio = element[3][0].toFixed(2);
    console.log(this.ratio);
    //this.currentId=id;
    if (element.length! > 0) {
      const config: ScrollToConfigOptions = {
        target: element[2][0],
      };

      this.scrollToService.scrollTo(config);
    }
  }
  //for scale up purpose
  triggerScrollToV2(id: number, datavalue: number) {
    console.log(id);
    if (id <= 0) {
      return;
    } else {
      id = id - 1;
      console.log(id);

      let element = this.answer.ls3[id];
      if (datavalue > 0 && this.storeNumber < element[3].length - 1) {
        this.storeNumber = this.storeNumber + 1;
      } else if (datavalue < 0 && this.storeNumber > 0) {
        this.storeNumber = this.storeNumber - 1;
      }
      console.log('store number is');
      console.log(this.storeNumber);
      console.log(element);
      if ((this.storeNumber >= element[3].length && datavalue > 0) || (this.storeNumber < 0 && datavalue < 0)) {
        console.log('fail ver 2');
        return;
      } else {
        this.ratio = element[3][this.storeNumber].toFixed(2);
        console.log(this.ratio);
        if (element.length! > 0) {
          const config: ScrollToConfigOptions = {
            target: element[2][this.storeNumber],
          };

          this.scrollToService.scrollTo(config);
        }
      }
    }
  }
  scrollPrevious() {
    this.triggerScrollToV2(this.currentId, -1);
  }
  scrollNext() {
    this.triggerScrollToV2(this.currentId, 1);
  }
  shouldHighlight(id: number) {
    if (id <= this.answer.ls1.length) {
      if (this.answer.ls3[id - 1][1] > 0) {
        return true;
      } else return false;
    }
    return false;
  }
  shouldHighlight2(id: number) {
    if (this.sameline.indexOf(id) === -1) {
      return false;
    } else return true;
  }
}
