import { Component, OnInit, Input } from '@angular/core';
import { Artist, Album, ApiService } from '../api.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-artist',
  templateUrl: './artist.component.html',
  styleUrls: ['./artist.component.scss']
})
export class ArtistComponent implements OnInit {

  @Input() artist: Artist

  expanded = false;
  albums$: Observable<Album[]>;

  constructor(private api: ApiService) { }

  ngOnInit() {
    this.albums$ = this.api.getAlbums(this.artist.id);
  }

}
