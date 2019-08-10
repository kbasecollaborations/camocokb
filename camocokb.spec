/*
A KBase module: camocokb
*/

module camocokb {
    /* Ref to a sequence set
        @id ws KBaseGenomes.Genome
    */
    typedef string GenomeRef;

    /* Ref to a sequence set
       	@id ws KBaseGwasData.Associations
    */
    typedef string AssociationRef;

    /* Reference to an Assembly object in the workspace
    	@id ws KBaseGenomeAnnotations.Assembly
    */
    typedef string Assembly_ref;

    /* Ref to a sequence set
    	@id ws KBaseMatrices.ExpressionMatrix
    */
	typedef string Expr_matrix_ref;

	/* Ref to an ontology dictionary
	    @id ws KBaseOntology.OntologyDictionary
	*/
	typedef string ontology_dictionary;

	/*
        Typdefs for camoco objects
    */
    typedef string camoco_obj_name;

    typedef structure {
        camoco_obj_name object_name;
    } build_camoco_obj_out;

    typedef structure {
        GenomeRef genome_ref;
        AssociationRef association_ref;
        Expr_matrix_ref exp_matrix_ref;
        ontology_dictionary ontology;
        string workspace_name;
        int workspace_id;
        int window_size;
        int flank_limit;
    } CoexpNetworkInputParams;

    typedef structure {
        string filename;
        string refgen_name;
        string description;
    } BuildRefGenInputParams;

    typedef structure {
        string filename;
        string cob_name;
        string description;
        string refgen_name;
    } BuildCOBInputParams;

    typedef structure {
        string filename;
        string base_onotology_path;
        string ontology_name;
        string description;
        string refgen_name;
    } BuildOntologyInputParams;

    typedef structure {
        string file_name;
        camoco_obj_name obj_name;
        string description;
        camoco_obj_name refgen_name;
    } BuildGWASInputParams;

    typedef structure {
        int window_size;
        int flank_limit;
        string snp2gene_map;
        string strongest_attr;
    } FindGWASCoexpOverlapParams;

    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /* KBase Handling function */
    funcdef run_camocokb(CoexpNetworkInputParams params)
        returns (ReportResults output) authentication required;
    /* Camoco wrapping function */
    funcdef buildrefgen(BuildRefGenInputParams params)
        returns (build_camoco_obj_out output) authentication required;
    funcdef buildcob(BuildCOBInputParams params)
        returns (build_camoco_obj_out output) authentication required;
    funcdef buildontology(BuildOntologyInputParams params)
        returns (build_camoco_obj_out output) authentication required;
    funcdef buildgwas(BuildGWASInputParams params)
        returns (build_camoco_obj_out output) authentication required;
    funcdef overlapgwas(FindGWASCoexpOverlapParams params)
        returns (build_camoco_obj_out output) authentication required;
};
