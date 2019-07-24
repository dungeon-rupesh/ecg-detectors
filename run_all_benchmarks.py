"""
This script benchmarks all detectors with both the MIT database and the GU database.
You need to download both the MIT arrhythmia database from: https://alpha.physionet.org/content/mitdb/1.0.0/
and the GU database from: http://researchdata.gla.ac.uk/716/
Both need to be placed below this directory: "../mit-bih-arrhythmia-database-1.0.0/" and "../dataset_716".
"""
import numpy as np
import pathlib
from tester_MITDB import MITDB_test
from tester_GUDB import GUDB_test
from ecgdetectors import Detectors

current_dir = pathlib.Path(__file__).resolve()
mitdb_dir = str(pathlib.Path(current_dir).parents[1]/'mit-bih-arrhythmia-database-1.0.0')

do_test_MIT = True
do_test_GU  = True

if do_test_MIT:
    # MIT-BIH database testing
    mit_test = MITDB_test(mitdb_dir)
    mit_detectors = Detectors(360)
    
    # test single detector
    matched_filter_mit = mit_test.single_classifier_test(mit_detectors.matched_filter_detector, tolerance=0, print_results=True)
    np.savetxt('matched_filter_mit.csv', matched_filter_mit, fmt='%i', delimiter=',')

    # test all detectors on MITDB, will save results to csv, will take some time
    mit_results = mit_test.classifer_test_all()

    # McNemars stats test
    Z_value_mit = mit_test.mcnemars_test(mit_detectors.swt_detector, mit_detectors.two_average_detector, print_results = True)

if do_test_GU:
    # GUDB database testing
    gu_test = GUDB_test()
    gu_detectors = Detectors(250)
    
    swt_gudb = gu_test.single_classifier_test(gu_detectors.swt_detector, tolerance=0, config='chest_strap')
    
    gu_results = gu_test.classifer_test_all(tolerance=0, config='chest_strap')
    
    Z_value_gu = gu_test.mcnemars_test(gu_detectors.swt_detector, gu_detectors.two_average_detector, print_results = True)