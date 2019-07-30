import { Component, OnInit, Input } from '@angular/core';
import { Album, Song, ApiService } from '../api.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-album',
  templateUrl: './album.component.html',
  styleUrls: ['./album.component.scss']
})
export class AlbumComponent implements OnInit {

  @Input() album: Album

  expanded = false;
  songs$: Observable<Song[]>;

  constructor(private api: ApiService) { }

  ngOnInit() {
    this.songs$ = this.api.getSongs(this.album.id);
  }

}
