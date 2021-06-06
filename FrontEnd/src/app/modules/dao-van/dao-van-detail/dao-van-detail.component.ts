import { Component, OnInit } from '@angular/core';
import {DaovanServiceService} from '../daovan-service.service'

import { CommonModule } from '@angular/common';

import { SharedModule } from '@app/shared/shared.module';
//import { stringify } from '@angular/core/src/util';

import { TranslateModule } from '@ngx-translate/core';
import { ActivatedRoute, Router } from '@angular/router';
import { identity } from 'lodash';
//import throttleByAnimationFrame from 'ng-zorro-antd/core/util/throttleByAnimationFrame';
import { FileService } from '@../../../src/app/shell/shell-routing-service';
import { SessionToHistoryService } from '@app/shared/components/session-to-history.service';
@Component({
  selector: 'app-dao-van-detail',
  templateUrl: './dao-van-detail.component.html',
  styleUrls: ['./dao-van-detail.component.scss'],
  providers:[DaovanServiceService]
})
export class DaoVanDetailComponent implements OnInit {
  public params:any;
  private sessionId:any;
 public data1:any;
  public dataForDiff:any;
  public currentId: number;
  public StoreNumber: number;
  public characterList1: any[];
  public characterList2: any[];
  public listchar: any[];
  public file1:any[];
  public answer: any;
  public option: any[];
  public SelectedOption: number;
  public hitrate: any[];
  public trolling: boolean;
  public stt:any[];
  ListHitRate: any[];
  public file1Name: any;
  public ratio: any[];
  public safetyFlag=true;
  HighestHitRate: any;
  
  public data:Array<any>=[
    {
      name:'yuragi sou',
      id:1,
      genre:'ecchi',
      ratio:10
    },
    {
      name:'to love ru',
      id:2,
      genre:'ecchi',
      ratio:20,
    },
    {
      name:'nisekoi',
      id:3,
      genre:'ecchi',
      ratio:30,
    },
    {
      name:'gotoubun',
      id:4,
      genre:'ecchi',
      ratio:25
    }
  ];
  //public File1Name= this.data;
  public FileList2: Array<any>;
  public ListAllFile:any[];
  
  constructor(
    //public file1Name:any;

    private router: Router,
    private route: ActivatedRoute,
    private fileService: FileService,
    private activatedRoute: ActivatedRoute //private matDialog: MatDialog
  ) {
    this.characterList1 = [];
    this.SelectedOption = 0;
    this.ListHitRate = [];
    this.ratio = null;
    this.StoreNumber = 0;
    this.currentId = -1;
    this.answer = {
      ls1: null,
      ls2: null,
      ls3: null,
    };
    this.activatedRoute.queryParams.subscribe((params) => {
      console.log('new file');
      console.log(params);
     
      this.params = params;
      if (params.filename1 == undefined && params.File1Name == undefined) {
        console.log('false');
        console.log(this.router.getCurrentNavigation());
        if (this.router.getCurrentNavigation().extras.state != null) {
          this.data1 = this.router.getCurrentNavigation().extras.state.data;
          console.log(this.data1);
          console.log('end here');
          this.file1Name = this.data1.File1Name;
          this.FileList2=[];
      for( var i = 0; i < this.data1.ListFileName.length; i++)
      {
        let temp  ={
          name:this.data1.ListFileName[i],
          ratio:this.data1.AllFileRatio[i]
        } 
        this.FileList2.push(temp);
      }
      
      this.ListAllFile = this.data1.ListAllFile;
      this.file1 = this.data1.data;
      this.stt = this.data1.stt;
    
      //this.data1 = this.params.data;
      
      console.log(this.ListAllFile);
      let temp = [];
      this.dataForDiff={
        file1:this.data1.file1,
        
        ListFile:this.data1.ListFile
        
        }
      console.log("this is new data for diff");
      console.log(this.dataForDiff);
      }
      else{
        console.log("different escape");
        if (this.params.file1Name != undefined) {
          console.log(this.params.File1Name);
          this.file1Name = this.params.File1Name;
          this.FileList2 = this.params.fileList2;
          this.ListAllFile = this.params.ListAllFile;
          this.file1 = this.params.file1;
          this.stt = this.params.stt;
          
          this.data1 = this.params.data;
          console.log('true');
          console.log(this.ListAllFile);
          let temp = [];
          this.dataForDiff={
            file1:this.file1,
            data:this.data1,
            stt:this.stt,
          }
          console.log("this is new data for diff");
          console.log(this.dataForDiff);
          temp.push(this.params.listfile);
          
          /*let data = {
            id: this.params.id,
            filename1: this.params.filename1,
            listfile: temp,
            choice: 1,
          };
          console.log('data is');
          console.log(data);
          this.fileService.checkPlagiasm(data).subscribe(
            (data: any) => {
              this.data = data;
              this.trolling = false;
    
              // this.getFirstSentences();
    
              // this.ShowResult(0);
              // this.createOptionList();
            },
            (error) => {}
          );*/
         }
         else
         {
           console.log("dieeeeeeeeeeeeeeeeeee");

           this.safetyFlag=false;
         }
      }
      }
      // Print the parameter to the console.
    });
  }
  


  ngOnInit() {
    if(!this.safetyFlag){
      
      this.route.params.subscribe(params => {
        console.log(params) //log the entire params object
        console.log(params['id']) //log the value of id
        let data = Number(params['id']);
        this.fileService.getResult(data).subscribe((data:any)=>{
          this.data1 = data;
          this.file1Name = this.data1.File1Name;
          this.FileList2=[];
      for( var i = 0; i < this.data1.ListFileName.length; i++)
      {
        let temp  ={
          name:this.data1.ListFileName[i],
          ratio:this.data1.AllFileRatio[i]
        } 
        this.FileList2.push(temp);
      }
      
      this.ListAllFile = this.data1.ListAllFile;
      this.file1 = this.data1.data;
      this.stt = this.data1.stt;
    
      //this.data1 = this.params.data;
      
      console.log(this.ListAllFile);
      let temp = [];
      this.dataForDiff={
        file1:this.data1.file1,
        
        ListFile:this.data1.ListFile
        
        }
      console.log("this is new data for diff");
      console.log(this.dataForDiff);
        })
      });
    }
    
    //this.forgodTest();

    

    
    
  }
}
