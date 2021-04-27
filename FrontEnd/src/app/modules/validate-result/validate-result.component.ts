import { Component, OnInit, NgModule } from '@angular/core';
import {} from '@angular/core';
import { CommonModule } from '@angular/common';
import { ViewportScroller } from '@angular/common';
import { NgZorroAntdModule } from 'ng-zorro-antd';
import { SharedModule } from '@app/shared/shared.module';
import { stringify } from '@angular/core/src/util';
import { ScrollToService, ScrollToConfigOptions } from '@nicky-lenaers/ngx-scroll-to';
import { TranslateModule } from '@ngx-translate/core';
import { ActivatedRoute, Router } from '@angular/router';
import { identity } from 'lodash';
import throttleByAnimationFrame from 'ng-zorro-antd/core/util/throttleByAnimationFrame';
import { FileService } from '@../../../src/app/shell/shell-routing-service';
@Component({
  selector: 'app-validate-result',
  templateUrl: './validate-result.component.html',
  styleUrls: ['./validate-result.component.scss'],
})
export class ValidateResultComponent implements OnInit {
  public data: any;
  public tdata: any;
  private tempdata: any;
  private currentId: string;
  private StoreNumber: number;
  public characterList1: any[];
  public characterList2: any[];
  public listchar: any[];
  private sameline: any[];
  public answer: any;
  public option: any[];
  public SelectedOption: number;
  public hitrate: any[];
  public trolling: boolean;
  ListHitRate: any[];
  public file1Name: any;
  public ratio: any[];
  HighestHitRate: any;
  public params: any;
  ngOnInit() {
    //this.forgodTest();

    this.characterList1 = [];
    this.SelectedOption = 0;
    this.ListHitRate = [];
    this.ratio = null;

    this.answer = {
      ls1: null,
      ls2: null,
      ls3: null,
    };
    if (this.params != undefined) {
      console.log(this.params.filename1);
      console.log('true');
      let temp = [];
      temp.push(this.params.listfile);
      let data = {
        id: this.params.id,
        filename1: this.params.filename1,
        listfile: temp,
        choice: 1,
      };
      console.log('data is');
      console.log(data);
      this.fileService.checkPlagiasm(data).subscribe((data: any) => {
        this.data = data;
        this.trolling = false;

        this.getFirstSentences();

        this.ShowResult(0);
        this.createOptionList();
      });
    } else if (this.data != null) {
      this.getFirstSentences();
      this.ShowResult(0);
      console.log('escape success');
      this.createOptionList();
      console.log('this ls1 is');
      console.log(this.answer.ls1);
    } else {
      console.log('not really');
      this.ChangeOption();
    }
  }
  ChangeOption() {
    this.characterList2 = ['kurogane yaiba', 'kurosaki ichigo', 'monkey D luffy', 'uzumaki naruto'];
    //console.log('escape fail');
    let temp: {
      id: number;
      data: string;
    };
    console.log(this.characterList2.length);
    console.log(this.characterList1);
    this.characterList1 = [];
    for (var i = 0; i < this.characterList2.length; i++) {
      temp = {
        id: i,
        data: this.characterList2[i],
      };
      this.characterList1.push(temp);
    }

    console.log(this.characterList1);
  }
  createOptionList() {
    let temp: {
      id: number;
      data: string;
    };

    if (this.data != null) {
      for (var i = 0; i < this.data.ListFileName.length; i++) {
        temp = {
          id: i,
          data: this.data.ListFileName[i],
        };
        this.characterList1.push(temp);
      }
    }
  }
  GetSelection(id: number) {
    this.SelectedOption = id;
  }
  confirmed() {
    console.log('this is');
    console.log(this.SelectedOption);
    this.ShowResult(this.SelectedOption);
  }
  getFirstSentences() {
    if (this.data != null) {
      this.file1Name = this.data.File1Name;
      this.tempdata = [];
      let temp: {
        id: number;
        data: string;
      };

      for (var i = 0; i < this.data.file1.length; i++) {
        temp = {
          id: i + 1,
          data: this.data.file1[i],
        };
        this.tempdata.push(temp);
      }
      this.answer.ls1 = this.tempdata;
    }
  }
  constructor(
    private viewportScroller: ViewportScroller,
    private scrollToService: ScrollToService,
    private router: Router,
    private route: ActivatedRoute,
    private fileService: FileService,
    private activatedRoute: ActivatedRoute
  ) {
    this.activatedRoute.queryParams.subscribe((params) => {
      console.log('new file');
      console.log(params);
      this.params = params;
      if (params.filename1 == undefined) {
        console.log('false');
        console.log(this.router.getCurrentNavigation());
        if (this.router.getCurrentNavigation().extras.state != null) {
          this.data = this.router.getCurrentNavigation().extras.state.data;
          console.log(this.data);
        }
        this.trolling = false;
      }
      // Print the parameter to the console.
    });
  }

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
  triggerScrollTo(id: number) {
    id = id - 1;
    console.log(id);

    let element = this.answer.ls3[id];

    console.log(this.ratio);
    this.ratio = element[3][0];
    if (element.length! > 0) {
      const config: ScrollToConfigOptions = {
        target: element[2][0],
      };

      this.scrollToService.scrollTo(config);
    }
  }
  checkline(id: number) {
    if (this.answer.ls3[id].length > 0) return true;
    else return false;
  }
  Comeback() {
    this.router.navigate(['daovan'], { replaceUrl: true });
  }
  shouldHighlight(id: number) {
    /*if (this.answer.ls3[id].length > 0)
     {
       console.log(id);
       
       return true;
     }

    else 
      return false;*/

    if (id <= this.answer.ls1.length) {
      if (this.answer.ls3[id - 1][1] > 0) {
        return true;
      } else return false;
    }
    return false;
  }
  settrue() {
    console.log('pass');
    this.trolling = true;
  }
  shouldHighlight2(id: number) {
    if (this.sameline.indexOf(id) === -1) {
      return false;
    } else return true;
  }
  choose(choice: string) {
    console.log(choice);
  }
  /*onClick3($element): void {
    console.log($element);
    $element.scrollIntoView({behavior: "smooth", block: "start", inline: "nearest"});
  }*/
  forgodTest() {
    this.listchar = [
      { line: 0, length: 2, list: [0, 7] },
      { line: 1, length: 0, list: null },
      {
        line: 2,
        length: 1,
        list: [7],
      },
      {
        line: 3,
        length: 1,
        list: [12],
      },
    ];

    this.StoreNumber = 0;
    this.characterList2 = [
      'kurogane yaiba',
      'mod',
      'mod',
      'mod',
      'kurosaki ichigo',
      'mod',
      'mod',
      'monkey D luffy',
      'mod',
      'mod',
      'mod',
      'mod',
      'uzumaki naruto',
    ];
    this.characterList1 = ['kurogane yaiba', 'kurosaki ichigo', 'monkey D luffy', 'uzumaki naruto'];

    this.tempdata = [];
    let tempdata2 = [];
    let ans: {
      ls1: any;
      ls2: any;
      ls3: any;
    };
    ans = { ls1: 3, ls2: 4, ls3: 5 };
    let index = 0;
    ans.ls3 = this.listchar;
    let temp: {
      id: number;
      data: string;
    };
    for (var i = 0; i < this.characterList1.length; i++) {
      temp = {
        id: index,
        data: this.characterList1[i],
      };
      this.tempdata.push(temp);

      for (var j = 0; j < this.listchar[index].length; j++) {
        if (this.sameline.indexOf(this.listchar[index].list[j]) === -1) {
          this.sameline.push(this.listchar[index].list[j]);
        }
      }
      index = index + 1;
    }

    ans.ls1 = this.tempdata;
    index = 0;
    for (var i = 0; i < this.characterList2.length; i++) {
      temp = {
        id: index,
        data: this.characterList2[i],
      };
      tempdata2.push(temp);
      index = index + 1;
      //console.log(this.listchar[index].length);
    }
    ans.ls2 = tempdata2;

    this.tdata;
    this.tdata = this.tempdata;
    this.answer = ans;
    console.log(this.sameline);
  }
  /*this.answer=
      {
        ls1:data.file1,
        ls2:data.ListFile[0].data,
        ls3:data.ListFile[0].stt
      }*/
  /*forgodlvlMax(num : number)
{
  this.sameline=[];
      let data = this.data;
      console.log(this.data);

      
      this.tempdata=[];
      let temp: {
        id: number;
        data: string;
      };
      let index = 0;
      for (var i = 0; i < this.data.file1.length; i++) {
    
        temp = {
          id: index+1,
          data: this.data.file1[i]
        };
        this.tempdata.push(temp);
        
        
        
        for(var j = 0; j < this.data.ListFile[num].stt[i][1]; j++)
        {
          console.log('begin');
          console.log(this.data.ListFile[num].stt[i][2][j])
          if (this.sameline.indexOf(this.data.ListFile[num].stt[i][2][j]) === -1) {
            this.sameline.push(this.data.ListFile[num].stt[i][2][j]);
        }
      }
        index = index + 1;
      }
      index = 0;
      let tempdata2 = [];
      for (var i = 0; i < this.data.ListFile[num].data.length; i++) {
    
        temp = {
          id: index+1,
          data: this.data.ListFile[num].data[i]
        };
        tempdata2.push(temp);
        index = index + 1;
        //console.log(this.listchar[index].length);
       
      }
      this.answer=
      {
        ls1:this.tempdata,
        ls2:tempdata2,
        ls3:data.ListFile[0].stt
      }
      console.log(this.answer.ls1);
      console.log(this.answer.ls2);
      console.log(this.answer.ls3);
     
      console.log(data);
}*/
  ShowResult(num: number) {
    this.sameline = [];
    let data = this.data;
    console.log(this.data);

    if (this.data != null) {
      let temp: {
        id: number;
        data: string;
      };
      let index = 0;
      for (var i = 0; i < this.data.file1.length; i++) {
        if (this.data.ListFile[num].stt[i] != undefined) {
          for (var j = 0; j < this.data.ListFile[num].stt[i][1]; j++) {
            console.log(this.data.ListFile[num].stt[i][2][j]);
            if (this.sameline.indexOf(this.data.ListFile[num].stt[i][2][j]) === -1) {
              this.sameline.push(this.data.ListFile[num].stt[i][2][j]);
            }
          }
        }
      }

      let tempdata2 = [];
      for (var i = 0; i < this.data.ListFile[num].data.length; i++) {
        temp = {
          id: index + 1,
          data: this.data.ListFile[num].data[i],
        };
        tempdata2.push(temp);
        index = index + 1;
        //console.log(this.listchar[index].length);
      }
      this.answer.ls2 = tempdata2;
      this.answer.ls3 = data.ListFile[num].stt;
      /*this.answer=
      {
        ls1:this.tempdata,
        ls2:tempdata2,
        ls3:data.ListFile[0].stt
      }
      console.log(this.answer.ls1);
      console.log(this.answer.ls2);
      console.log(this.answer.ls3);
     */
      console.log(data);
    } else {
      this.forgodTest();
    }
  }
  ExportEmail() {
    let temp = 0;
    let countlist = [];
    this.hitrate = [];
    console.log(this.answer.ls2.length);
    console.log(this.answer);
    for (var i = 0; i < this.data.ListFile.length; i++) {
      temp = 0;
      for (var j = 0; j < this.data.ListFile[i].stt.length; j++) {
        if (this.data.ListFile[i].stt[j][1] > 0) {
          temp = temp + 1;
        }
      }
      countlist.push(temp);
      let totalrate = temp / this.answer.ls1.length;
      this.hitrate.push(totalrate * 100);
    }
    console.log('final result is');
    console.log(this.hitrate);
    let HighestHitRate = 0;
    for (var i = 0; i < this.hitrate.length; i++) {
      if (this.hitrate[i] >= this.hitrate[HighestHitRate]) {
        HighestHitRate = i;
      }
    }

    var result = {
      File1Name: this.file1Name,
      name: this.data.ListFileName,
      HitRate: this.hitrate,
      Highest: HighestHitRate,
      count: countlist,
      id: localStorage.getItem('id'),
    };

    this.fileService.ExportResultToEmail(result).subscribe((data: any) => {
      console.log('success');
    });
  }
}
