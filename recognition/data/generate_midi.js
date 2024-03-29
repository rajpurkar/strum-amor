var fs = require('fs');
var jsmidgen = require('jsmidgen');

var NOTE_DURATION = 1000;

Midi = function() {
	var d = new Date();
	this.t = d.getTime();
	fs.mkdirSync("midi_files/"+this.t);
};

// notes is an array of notes, e.g. ['c4, 'e4', 'g4']
Midi.prototype.addChord = function(notes, duration) {
	this.track.addNoteOn(0, notes[0], this.time);
	for (var i = 1; i < notes.length; i++) {
		this.track.addNoteOn(0, notes[i]);
	}
	this.time += duration;
	this.track.addNoteOff(0, notes[0], this.time);
	for (i = 1; i < notes.length; i++) {
		this.track.addNoteOff(0, notes[i]);
	}
};

Midi.prototype.writeFile = function(chordname) {
	fs.writeFileSync("midi_files/"+this.t+"/"+chordname+".mid", this.file.toBytes(), 'binary');
};

Midi.prototype.newFile = function(notes, chordname) {
	this.file = new jsmidgen.File();
	this.track = new jsmidgen.Track();
	this.file.addTrack(this.track);

	this.time = 0;
	if (typeof notes !== "undefined") {
		this.addChord(notes, NOTE_DURATION);
		if (typeof chordname !== "undefined") {
			this.writeFile(chordname);
		}
	}
};

module.exports = Midi;
