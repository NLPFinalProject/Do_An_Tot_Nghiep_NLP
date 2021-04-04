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
@Component({
  selector: 'app-validate-result',
  templateUrl: './validate-result.component.html',
  styleUrls: ['./validate-result.component.scss']
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
  private sameline:any[]
  public answer: any;
  ngOnInit() {
    //this.forgodTest();
    this.answer={
      ls1:null,
      ls2:null,
      ls3:null,
    }
    this.getFirstSentences();
    this.ShowResult(0); 
    
   

    
  }
  getFirstSentences()
  {
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
      }
      this.answer.ls1 = this.tempdata;
  }
  constructor(private viewportScroller: ViewportScroller, private scrollToService: ScrollToService,private router:Router,
    private route: ActivatedRoute,
    ) {
      
      this.data = this.router.getCurrentNavigation().extras.state.data;
      
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
    id = id;
    let element = this.answer.ls3[id];
    
    if (element.length! > 0) {
    
      const config: ScrollToConfigOptions = {
        target: element.list[0]
      };

      this.scrollToService.scrollTo(config);
    }
  }
  checkline(id: number) {
    if (this.answer.ls3[id].length > 0) return true;
    else 
      return false;
  }
  shouldHighlight(id:number)
  {
    
    /*if (this.answer.ls3[id].length > 0)
     {
       console.log(id);
       
       return true;
     }

    else 
      return false;*/
      if (this.answer.ls3[id-1][1] > 0)
     {
       console.log(id);
       
       return true;
     }

    else 
      return false;

  }
  shouldHighlight2(id:number)
  {
    if (this.sameline.indexOf(id) === -1) 
     {
       return false;
     }

    else 
      return true;

  }
  choose(choice: string)
  {
    console.log(choice);
  }
  /*onClick3($element): void {
    console.log($element);
    $element.scrollIntoView({behavior: "smooth", block: "start", inline: "nearest"});
  }*/
  forgodTest()
{
  this.listchar = [
    { line: 0, length: 2, list: [0,7] },
    { line: 1, length: 0, list: null },
    {
      line: 2,
      length: 1,
      list: [7]
    },
    {
      line: 3,
      length: 1,
      list: [12]
    }
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
    'uzumaki naruto'
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
      data: this.characterList1[i]
    };
    this.tempdata.push(temp);
    
    for(var j = 0; j < this.listchar[index].length; j++)
    {
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
      data: this.characterList2[i]
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
        ls2:data.fileName2[0].data,
        ls3:data.fileName2[0].stt
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
        
        
        
        for(var j = 0; j < this.data.fileName2[num].stt[i][1]; j++)
        {
          console.log('begin');
          console.log(this.data.fileName2[num].stt[i][2][j])
          if (this.sameline.indexOf(this.data.fileName2[num].stt[i][2][j]) === -1) {
            this.sameline.push(this.data.fileName2[num].stt[i][2][j]);
        }
      }
        index = index + 1;
      }
      index = 0;
      let tempdata2 = [];
      for (var i = 0; i < this.data.fileName2[num].data.length; i++) {
    
        temp = {
          id: index+1,
          data: this.data.fileName2[num].data[i]
        };
        tempdata2.push(temp);
        index = index + 1;
        //console.log(this.listchar[index].length);
       
      }
      this.answer=
      {
        ls1:this.tempdata,
        ls2:tempdata2,
        ls3:data.fileName2[0].stt
      }
      console.log(this.answer.ls1);
      console.log(this.answer.ls2);
      console.log(this.answer.ls3);
     
      console.log(data);
}*/
ShowResult(num : number)
{
  this.sameline=[];
      let data = this.data;
      console.log(this.data);

      
     
      let temp: {
        id: number;
        data: string;
      };
      let index = 0;
      for (var i = 0; i < this.data.file1.length; i++) {
        for(var j = 0; j < this.data.fileName2[num].stt[i][1]; j++)
        {
          console.log('begin');
          console.log(this.data.fileName2[num].stt[i][2][j])
          if (this.sameline.indexOf(this.data.fileName2[num].stt[i][2][j]) === -1) {
            this.sameline.push(this.data.fileName2[num].stt[i][2][j]);
        }
      }
        
      }
      
      let tempdata2 = [];
      for (var i = 0; i < this.data.fileName2[num].data.length; i++) {
    
        temp = {
          id: index+1,
          data: this.data.fileName2[num].data[i]
        };
        tempdata2.push(temp);
        index = index + 1;
        //console.log(this.listchar[index].length);
       
      }
      this.answer.ls2 = tempdata2;
      this.answer.ls3 = data.fileName2[0].stt
      /*this.answer=
      {
        ls1:this.tempdata,
        ls2:tempdata2,
        ls3:data.fileName2[0].stt
      }
      console.log(this.answer.ls1);
      console.log(this.answer.ls2);
      console.log(this.answer.ls3);
     */
      console.log(data);
}
}
