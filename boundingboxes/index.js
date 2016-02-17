var fk = require('fontkit');
var pp = require('pretty-print');
var decirc = require('smart-circular');
var _ = require('lodash');
var fse = require('fs-extra');

var gposLookupType = ['undefined', 'Single Adjustment', 'Pair Adjustment', 'Cursive Attachment', 'MarkToBase Attachment', 'MarkToLigature Attachment', 'MarkToMark Attachment', 'Context Positioning', 'Chained Context Positioning', 'Extension Positioning'];

// we will want to load the texts too
var example_text = "FiiFPiiPMiiMNiiN"

function fetch_fonts() {
	console.log('going to fetch fonts');

	return new Promise(function(resolve, reject) {
		var fonts = [];
		fse.walk('../fonts')
			.on('data', function(item) {
				if (item && item.path && item.path.indexOf('.ttf') === item.path.length - 4){
					fonts.push(item.path);
				}
			})
			.on('end', function() {
				resolve(fonts);
			});
	});
}

// https://www.microsoft.com/typography/otspec/chapter2.htm

/**
 * [single_adjustment description]
 * @param  {[type]} index_offset [description]
 * @param  {[type]} subTable     [description]
 * @return {[type]}              [description]
 */
function single_adjustment(index_offset, subTable) {
	console.log('Single Adjustment - - - - - - -');
	console.log(subTable[index_offset]);
}

/**
 * [pair_adjustment_version_1 description]
 * @param  {[type]} glyphId      [description]
 * @param  {[type]} nextGlyphId  [description]
 * @param  {[type]} index_offset [description]
 * @param  {[type]} subTable     [description]
 * @return {[type]}              [description]
 */
function pair_adjustment_version_1(glyphId, nextGlyphId, index_offset, subTable) {

}

/**
 * 
 * @param  {[type]} index_offset [description]
 * @param  {[type]} subTable     [description]
 * @return {[type]}              [description]
 */
function pair_adjustment_version_2(glyphId, nextGlyphId, index_offset, subTable) {
	// offset has the form 
	// 		{ version: 2, classRangeCount: 217, 
	// 		  classRangeRecord: [
	// 		  	// the start/end refers to the range of glyphIds
	//  		{ start: 16, end: 16, class: 1 },
	//   		{ start: 17, end: 17, class: 2 },
	//   		etc.
	//   	  ]
	//   	}
	// classDef1 is the lookup for the first Glyph for subTable.classRecords table
	// classDef2 is the lookup for the second Glyph for subTable.classRecords table
	
	console.log('pair adjustment classDef');
	console.log(subTable);
}

/**
 * Finds the offsets for the current glyph from the lookupList
 * @param  {[type]} glyphId     [description]
 * @param  {[type]} nextGlyphId [description]
 * @param  {[type]} lookupType  [description]
 * @param  {[type]} coverage    [description]
 * @param  {[type]} subTable    [description]
 * @return {[type]}             [description]
 */
function convert_coverage(glyphId, nextGlyphId, lookupType, coverage, subTable) {
	var result = null,
		index_offset = null;

	console.log('convert_coverage =-=-=-=-=-=-=-=-=-=-');

	// this is not necessarily true
	// if (lookupType === 2 && nextGlyphId === null){
	// 	console.log('pair set lookup, but no next glyph - we are done');
	// }

	// find the glyph id in the coverage list
	// 		if it does not exist then no further calculation needed for this lookup table for this glyph
	// using the index offset, add the glyphid to find the relevant offsets for that glyph
	// return the value!
	
	// there are two types of coverage lists - list (version 1) and ranges (version 2)
	if ( coverage.version === 1){
		console.log('list index');
		index_offset = _.indexOf(coverage.glyphs, glyphId);
	} else {
		console.log('range index');
		filtered = _.filter(coverage.rangeRecords, function (rng){
			return rng.start <= glyphId && rng.end >= glyphId;
		});
		console.log('filtered', filtered);
		index_offset = filtered.length === 0 ? null : filtered[0].startCoverageIndex;
	}

	console.log('index offset : ', index_offset, index_offset !== null && index_offset > -1);
	if (index_offset !== null && index_offset > -1){
		console.log('got here - lookup type', lookupType);

		switch(lookupType) {
			case 1:
				single_adjustment(index_offset, subTable);
				break;
			case 2:
				(subTable.version === 1) 
					? pair_adjustment_version_1(glyphId, nextGlyphId, index_offset, subTable) 
					: pair_adjustment_version_2(glyphId, nextGlyphId, index_offset, subTable);
				break;
			default:
				console.log('Lookup not yet supported : ', gposLookupType[lookupType]);
		}



		// // yeah its a big if statement, so sue me...
		// if (lookupType === 1){

		// 	console.log('Single Adjustment - - - - - - -');
		// 	console.log(subTable[index_offset]);

		// } else if (lookupType === 2){

		// 	console.log('Pair Adjustment - - - - - - - - next glyph :', nextGlyphId);

		// 	console.log('subtable version', subTable.version);
			
		// 	if (subTable.version === 1){
		// 		console.log('pair sets');
		// 		// pairSets is of type - restructure:LazyArray
		// 		// { secondGlyph: 111, value1: [Object], value2: {} },
		// 		var pair_sets = subTable.pairSets.get(index_offset);
		// 		var pair = _.filter(pair_sets, function(pair_set){
		// 			console.log('pair_set', pair_set);
		// 			return pair_set.secondGlyph === nextGlyphId;
		// 		});
		// 		console.log('pair', pair);
		// 	} else if (subTable.version === 2) {
		// 		console.log('classDef');

		// 		// offset has the form 
		// 		// 		{ version: 2, classRangeCount: 217, 
		// 		// 		  classRangeRecord: [
		// 		// 		  	// the start/end refers to the range of glyphIds
		// 		//  		{ start: 16, end: 16, class: 1 },
		// 		//   		{ start: 17, end: 17, class: 2 },
		// 		//   		etc.
		// 		//   	  ]
		// 		//   	}
		// 		// classDef1 is the lookup for the first Glyph for subTable.classRecords table
		// 		// classDef2 is the lookup for the second Glyph for subTable.classRecords table
		// 		// console.log('class def 1 offset', subTable.classDef1);
		// 		// console.log('class def 2 offset', subTable.classDef2);
		// 		// console.log('class records', subTable.classRecords);
		// 		var class_def_1 = _.filter(subTable.classDef1.classRangeRecord, function(def1) {
		// 			return def1.start <= glyphId && def1.start >= glyphId;
		// 		});
				
		// 		var class_def_2 = _.filter(subTable.classDef2.classRangeRecord, function(def2) {
		// 			return def2.start <= nextGlyphId && def2.start >= nextGlyphId;
		// 		});

				
				

		// 		// console.log('class 2 records', subTable.class2Record);
		// 		// classDef offsets are lookup tables to find which class a given glyph belongs to
		// 		// that class is then used to lookup the 
		// 	}

			
		// } else {
		// 	console.log('Lookup not yet supported : ', gposLookupType[lookupType]);
		// }
	}

	return result;
}

function show_font_details(font) {
	console.log(example_text);

	var lg = fk.openSync(font);

	var lay = lg.layout(example_text);

	console.log('-------------', font);

	// var ks = _.keys(lay);
	// var result = [];

	// for (var k of ks){
	// 	var kks = _.keys(k);
	// 	console.log(kks)
	// 	if (kks.length > 0){
	// 		newk = {};
	// 		newk[k] = kks;
	// 		k = newk;
	// 	}
	// 	result.push(k);
	// }

	// console.log('all keys',result);


	console.log(_.map(lay.glyphs, function(glyph) {
		return {
			kys: _.keys(glyph),
			id: glyph.id, 
			m: glyph._metrics, 
			bbox: glyph.path.bbox,
			kk: _.keys(glyph._path),
			af: glyph._font._layoutEngine.getAvailableFeatures(),
			k: _.keys(glyph._font)
		};
	}));
	console.log('positions ---- ',lay.positions);
	console.log('keys ----- ', _.keys(lay));

}

// function show_font_details(font) {
// 	console.log('showing details of font');

// 	var lg = fk.openSync(font);

// 	var lay = lg.layout(example_text);

// 	// console.log(lay.glyphs);

// 	console.log('-------------------------------------------------------------');
// 	for (var gid in lay.glyphs){
// 		gid = gid * 1; // convert to int...
// 		console.log('GLYPH =============', gid, lay.glyphs.length);
// 		var glyph = lay.glyphs[gid];
// 		var nextGlyphId = (gid < lay.glyphs.length) ? lay.glyphs[gid+1].id : null;
// 		console.log(glyph.path.bbox);
// 		console.log(glyph.id);
// 		console.log(glyph._metrics);

// 		console.log('FONT -=-=-=-=-=-=-=-');
// 		var gpos = glyph._font._tables.GPOS;
// 		console.log('GPOS : ', gpos);
// 		var lookupList = gpos.lookupList.items[0];
// 		for (var lookup of lookupList.subTables){
// 			console.log('COVERAGE : ',lookup.coverage);
// 			console.log('type: ', gposLookupType[lookupList.lookupType]);
// 			console.log('lookup type: ', lookup.version);
// 			console.log('lookup: ', convert_coverage(glyph.id, nextGlyphId, lookupList.lookupType, lookup.coverage, lookup));
// 		}
// 		// console.log('Lookups : ',thing._font._tables.GPOS);
// 	}
// 	console.log('-------------------------------------------------------------');

// 	// https://www.microsoft.com/typography/otspec/gpos.htm

// 	// returns a restructure/Struct
// 	// not sure how to access the properties yet
// 	// var thing = lay.glyphs[0]._font._tables.GPOS.lookupList;

// 	// var tables = lay.glyphs[0]._font._tables;
// 	// var gpos = tables.GPOS;

// 	// var scriptList = gpos.scriptList;
// 	// console.log('script list', scriptList);

// 	// var featureList = gpos.featureList;
// 	// console.log('feature list', featureList);
// 	// console.log('feature list, lookup list indices', featureList[0].feature.lookupListIndexes);


// 	// // lookup list tables
// 	// // https://www.microsoft.com/typography/otspec/chapter2.htm

// 	// // when adjusting glyphs, run through each lookuplist
// 	// var lookupList = gpos.lookupList.items[0]; // it's a 'Struct'
// 	// console.log('lookupType -- ', gposLookupType[lookupList.lookupType]);
// 	// console.log('lookup list -- ', lookupList);

// 	// // then run through each subtable of each lookuplist

// 	// //console.log('lookup list, subtables -- ', lookupList.subTables);
// 	// console.log('lookup list, coverage -- ', lookupList.subTables[0].coverage);
// 	// console.log('lookup list, class records [0] -- ', lookupList.classRecords);
// }

fetch_fonts()
	.then(function(fonts){
		// console.log(fonts);
		for (var font of fonts){
			console.log('details for font', font);
			show_font_details(font);
		}
	})
	.catch(function(err) {
		console.log(err);
	});




// // need to do this automatically
// var lg = fk.openSync('../fonts/luckiestguy/LuckiestGuy.ttf');

// var lay = lg.layout(example_text);

// // https://www.microsoft.com/typography/otspec/gpos.htm

// // returns a restructure/Struct
// // not sure how to access the properties yet
// // var thing = lay.glyphs[0]._font._tables.GPOS.lookupList;

// var tables = lay.glyphs[0]._font._tables;
// var gpos = tables.GPOS;

// var scriptList = gpos.scriptList;
// console.log('script list', scriptList);

// var featureList = gpos.featureList;
// console.log('feature list', featureList);
// console.log('feature list, lookup list indices', featureList[0].feature.lookupListIndexes);


// // lookup list tables
// // https://www.microsoft.com/typography/otspec/chapter2.htm

// // when adjusting glyphs, run through each lookuplist
// var lookupList = gpos.lookupList.items[0]; // it's a 'Struct'
// console.log('lookupType -- ', gposLookupType[lookupList.lookupType]);
// console.log('lookup list -- ', lookupList);

// // then run through each subtable of each lookuplist

// console.log('lookup list, subtables -- ', lookupList.subTables);
// console.log('lookup list, coverage -- ', lookupList.subTables[0].coverage);
// console.log('lookup list, class records [0] -- ', lookupList.classRecords);


// The GPOS table is organized so text processing clients can easily locate the features and lookups that apply to a particular script or language system. To access GPOS information, clients should use the following procedure:
// 
// 		Locate the current script in the GPOS ScriptList table.
// 		If the language system is known, search the script for the correct LangSys table; otherwise, use the script's default language system (DefaultLangSys table).
// 		The LangSys table provides index numbers into the GPOS FeatureList table to access a required feature and a number of additional features.
// 		Inspect the FeatureTag of each feature, and select the features to apply to an input glyph string.
// 		Each feature provides an array of index numbers into the GPOS LookupList table. Lookup data is defined in one or more subtables that contain information about specific glyphs and the kinds of operations to be performed on them.
// 		Assemble all lookups from the set of chosen features, and apply the lookups in the order given in the LookupList table.
// A lookup uses subtables to define the specific conditions, type, and results of a positioning action used to implement a feature. All subtables in a lookup must be of the same LookupType, as listed in the LookupType Enumeration table:

// LookupType Enumeration table for glyph positioning
// Value	Type	Description
// 1	Single adjustment	Adjust position of a single glyph
// 2	Pair adjustment	Adjust position of a pair of glyphs
// 3	Cursive attachment	Attach cursive glyphs
// 4	MarkToBase attachment	Attach a combining mark to a base glyph
// 5	MarkToLigature attachment	Attach a combining mark to a ligature
// 6	MarkToMark attachment	Attach a combining mark to another mark
// 7	Context positioning	Position one or more glyphs in context
// 8	Chained Context positioning	Position one or more glyphs in chained context
// 9	Extension positioning	Extension mechanism for other positionings
// 10+	Reserved	For future use (set to zero)
